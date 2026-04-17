import argparse
from datetime import datetime, timedelta

from .config import (
    BOLD,
    BLUE,
    CYAN,
    DEFICIENT,
    DIM,
    GREEN,
    INSUFFICIENT,
    LEVEL_LABELS,
    RED,
    RESET,
    SEVERE,
    SUFFICIENT,
    TOXIC,
    YELLOW,
)
from .storage import (
    get_latest_level,
    get_today,
    is_deficient,
    load_data,
    save_data,
    sun_target,
    supp_target,
    today_key,
)


def get_level_label(val):
    for (lo, hi), label in LEVEL_LABELS.items():
        if lo <= val < hi:
            return label
    return "UNKNOWN"


def get_level_color(val):
    if val < SEVERE:
        return RED
    if val < DEFICIENT:
        return RED
    if val < INSUFFICIENT:
        return YELLOW
    if val < SUFFICIENT:
        return YELLOW
    if val < TOXIC:
        return GREEN
    return RED


def bar(current, target, width=30):
    ratio = min(current / target, 1.0) if target > 0 else 0
    filled = int(ratio * width)
    return f"[{'█' * filled}{'░' * (width - filled)}] {current}/{target}"


def cmd_status(_args):
    data = load_data()
    today = get_today(data)
    level = get_latest_level(data)
    color = get_level_color(level) if level else ""

    print(f"\n{BOLD}  ☀  Vitamin D Dashboard{RESET}")
    print(f"  {'─' * 38}")

    if level:
        print(
            f"  Latest Level:  {color}{BOLD}{level} ng/mL{RESET}  ({color}{get_level_label(level)}{RESET})"
        )
        target = 30
        print(f"  To Sufficiency:{GREEN} {bar(level, target)}{RESET}")
        if level < INSUFFICIENT:
            deficit = target - level
            weeks = max(1, round(deficit / 5))
            print(
                f"  Est. Recovery: {CYAN}~{weeks} weeks{RESET} with proper supplementation"
            )
    else:
        print(f"  {DIM}No test results logged yet. Run: vitd setup{RESET}")

    print()
    s_target = sun_target(level)
    print(f"  Sun Today:     {YELLOW}{bar(today['sun_minutes'], s_target)}{RESET} min")
    supp_total = sum(s["iu"] for s in today["supplements"])
    d_target = supp_target(level)
    print(f"  Supplement:    {BLUE}{bar(supp_total, d_target)}{RESET} IU")

    if today["notes"]:
        print(f"\n  {DIM}Notes:{RESET}")
        for n in today["notes"]:
            print(f"    {DIM}• {n}{RESET}")

    print()


def cmd_log_sun(args):
    data = load_data()
    today = get_today(data)
    today["sun_minutes"] += args.minutes
    save_data(data)
    level = get_latest_level(data)
    s_target = sun_target(level)
    remaining = max(0, s_target - today["sun_minutes"])
    if remaining > 0:
        print(
            f"  ☀  Logged {YELLOW}{args.minutes} min{RESET} sun. {CYAN}{remaining} min more{RESET} to hit today's target."
        )
    else:
        print(
            f"  ☀  Logged {YELLOW}{args.minutes} min{RESET} sun. {GREEN}Target reached!{RESET}"
        )


def cmd_log_supplement(args):
    data = load_data()
    today = get_today(data)
    today["supplements"].append(
        {"iu": args.iu, "time": datetime.now().strftime("%H:%M")}
    )
    save_data(data)
    print(f"  💊 Logged {BLUE}{args.iu} IU{RESET} supplement.")


def cmd_log_note(args):
    data = load_data()
    today = get_today(data)
    today["notes"].append(args.text)
    save_data(data)
    print(f"  📝 Note saved.")


def cmd_test(args):
    data = load_data()
    data["tests"].append({"date": today_key(), "level": args.level})
    save_data(data)
    color = get_level_color(args.level)
    label = get_level_label(args.level)
    print(
        f"\n  🧪 Test result: {color}{BOLD}{args.level} ng/mL{RESET} ({color}{label}{RESET})"
    )
    if args.level < SEVERE:
        print(
            f"  {RED}⚠  Critical! See a doctor immediately for prescription loading doses.{RESET}"
        )
    elif args.level < DEFICIENT:
        print(
            f"  {RED}⚠  Severe deficiency. Prescription supplements likely needed.{RESET}"
        )
    elif args.level < INSUFFICIENT:
        print(
            f"  {YELLOW}⚠  Deficient. High-dose OTC or prescription recommended.{RESET}"
        )
    elif args.level < SUFFICIENT:
        print(f"  {YELLOW}⚠  Insufficient. Daily supplementation recommended.{RESET}")
    else:
        print(
            f"  {GREEN}✓  Good levels. Maintain with daily supplements and sun.{RESET}"
        )
    print()


def cmd_remind(_args):
    data = load_data()
    today = get_today(data)
    now = datetime.now()
    hour = now.hour
    level = get_latest_level(data)
    s_target = sun_target(level)

    print(f"\n  {BOLD}🔔 Reminders{RESET}")
    print(f"  {'─' * 30}")

    reminders = []

    if 10 <= hour <= 14 and today["sun_minutes"] < s_target:
        remaining = s_target - today["sun_minutes"]
        reminders.append(
            f"☀  Step outside NOW! UV is at peak. Need {remaining} more min of sun."
        )

    if hour >= 14 and today["sun_minutes"] < s_target:
        remaining = s_target - today["sun_minutes"]
        reminders.append(
            f"☀  You missed peak sun hours. Try to get {remaining} min tomorrow 10am-2pm."
        )

    if hour < 10:
        reminders.append("☀  Peak sun window is 10am-2pm. Set an alert for later!")

    supp_total = sum(s["iu"] for s in today["supplements"])
    d_target = supp_target(level)
    if supp_total < d_target:
        remaining = d_target - supp_total
        reminders.append(
            f"💊 Take your Vitamin D supplement ({remaining} IU remaining today)."
        )

    if is_deficient(level):
        reminders.append("🩺 Book a follow-up blood test in 6-8 weeks.")
        reminders.append("🥛 Include calcium-rich foods with your supplement.")

    if not reminders:
        print(f"  {GREEN}All caught up! Nothing pending right now.{RESET}")
    else:
        for r in reminders:
            print(f"  {r}")

    print()


def cmd_history(args):
    data = load_data()
    days = args.days

    print(f"\n  {BOLD}📋 Last {days} Days{RESET}")
    print(f"  {'─' * 50}")
    print(f"  {'Date':<12} {'☀ Sun':>8} {'💊 Supp':>10} {'Notes':>20}")
    print(f"  {'─' * 50}")

    for i in range(days):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        if d in data["daily"]:
            entry = data["daily"][d]
            supp = sum(s["iu"] for s in entry["supplements"])
            notes = ", ".join(entry["notes"][:2]) if entry["notes"] else ""
            marker = (
                f"{GREEN}✓{RESET}" if entry["sun_minutes"] >= 15 else f"{RED}✗{RESET}"
            )
            print(
                f"  {d:<12} {marker} {entry['sun_minutes']:>4}m  {supp:>6} IU  {notes}"
            )
        else:
            print(f"  {d:<12} {RED}✗   —       — IU{RESET}")

    print()

    if data["tests"]:
        print(f"  {BOLD}Test History:{RESET}")
        for t in data["tests"]:
            color = get_level_color(t["level"])
            print(
                f"  {t['date']}  {color}{t['level']} ng/mL{RESET} ({get_level_label(t['level'])})"
            )
        print()


def cmd_tips(_args):
    data = load_data()
    level = get_latest_level(data)

    print(f"\n  {BOLD}💡 Personalized Tips{RESET}")
    print(f"  {'─' * 40}")

    if level and level < INSUFFICIENT:
        print(f"""
  Your level ({level} ng/mL) is {RED}critically low{RESET}. Here's your action plan:

  {BOLD}Supplements:{RESET}
    • Take 2000-4000 IU D3 daily (or as prescribed)
    • Take with the {BOLD}largest meal{RESET} of the day (fat improves absorption)
    • Pair with K2 (100mcg) to direct calcium to bones
    • Don't take on empty stomach — waste of money

  {BOLD}Sun:{RESET}
    • 20-30 min midday sun (10am-2pm) on bare arms/face
    • Darker skin = more time needed
    • Glass blocks UV-B — step {BOLD}outside{RESET}, not just near a window
    • Clouds reduce UV by only ~20-30%

  {BOLD}Diet:{RESET}
    • Fatty fish (salmon, sardines, mackerel) — 2-3x/week
    • Egg yolks, fortified milk, fortified cereals
    • UV-exposed mushrooms (leave them in sun 15 min before cooking)

  {BOLD}Lifestyle:{RESET}
    • Set a daily alarm: "vitamin D" at noon
    • Walk during lunch break — counts as sun + exercise
    • Re-test in 6-8 weeks

  {BOLD}Medical:{RESET}
    • If level < 10, ask about prescription loading doses
    • Get calcium and B12 checked too
    • Magnesium helps D activation — consider supplementing
""")
    elif level and level < SUFFICIENT:
        print(f"""
  Your level ({level} ng/mL) is {YELLOW}below optimal{RESET}.

  • Take 1000-2000 IU D3 daily with a meal
  • 15 min midday sun on exposed skin, 3-4x/week
  • Re-test in 3 months
""")
    elif level:
        print(f"""
  Your level ({level} ng/mL) is {GREEN}good{RESET}!

  • Maintain with 1000 IU D3 daily
  • Keep getting regular sun exposure
  • Test annually
""")
    else:
        print(f"""
  {DIM}Log your test result first:{RESET}  vitd setup --level <level>

  General tips:
  • 15-20 min midday sun, 3-4x/week
  • 1000-2000 IU D3 daily with a fatty meal
  • Re-test every 3-6 months
""")
    print()


def cmd_setup(args):
    level = args.level
    data = load_data()
    if not data["tests"]:
        data["tests"].append({"date": today_key(), "level": level})
        save_data(data)
    print(f"\n  {GREEN}✓ Setup complete!{RESET}")
    print(
        f"  {BOLD}Vitamin D level set to:{RESET} {RED}{level} ng/mL{RESET} ({get_level_label(level)})"
    )
    print(f"""
  {BOLD}Quick Start:{RESET}
    vitd              Show dashboard
    vitd sun 20       Log 20 min of sun
    vitd supp 2000    Log 2000 IU supplement
    vitd remind       Check what you need to do
    vitd tips         Get personalized tips
    vitd history      View past 7 days
    vitd test 30      Update your test result
    vitd note "text"  Add a daily note

  {CYAN}Add to your shell for daily reminders:{RESET}
    echo 'vitd remind' >> ~/.bashrc
""")


def main():
    parser = argparse.ArgumentParser(
        prog="vitd",
        description="Vitamin D deficiency tracker & assistant",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Today's dashboard")

    sp_sun = sub.add_parser("sun", help="Log sun exposure (minutes)")
    sp_sun.add_argument("minutes", type=int, help="Minutes of sun exposure")

    sp_supp = sub.add_parser("supp", help="Log supplement intake (IU)")
    sp_supp.add_argument("iu", type=int, help="IU of Vitamin D3")

    sp_note = sub.add_parser("note", help="Add a note")
    sp_note.add_argument("text", help="Note text")

    sp_test = sub.add_parser("test", help="Log new blood test result")
    sp_test.add_argument("level", type=float, help="Vitamin D level (ng/mL)")

    sub.add_parser("remind", help="Show active reminders")
    sub.add_parser("tips", help="Personalized tips based on your level")

    sp_hist = sub.add_parser("history", help="View past logs")
    sp_hist.add_argument(
        "--days", type=int, default=7, help="Number of days (default: 7)"
    )

    sp_setup = sub.add_parser("setup", help="Initial setup")
    sp_setup.add_argument(
        "--level", type=float, required=True, help="Initial vit D level (ng/mL)"
    )

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "sun": cmd_log_sun,
        "supp": cmd_log_supplement,
        "note": cmd_log_note,
        "test": cmd_test,
        "remind": cmd_remind,
        "tips": cmd_tips,
        "history": cmd_history,
        "setup": cmd_setup,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        cmd_status(args)
