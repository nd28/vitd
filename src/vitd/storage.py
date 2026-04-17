import json
import os
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.vitd")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tests": [], "daily": {}}
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def today_key():
    return datetime.now().strftime("%Y-%m-%d")


def get_today(data):
    key = today_key()
    if key not in data["daily"]:
        data["daily"][key] = {"sun_minutes": 0, "supplements": [], "notes": []}
    return data["daily"][key]


def get_latest_level(data):
    return data["tests"][-1]["level"] if data["tests"] else None


def is_deficient(level):
    return level is not None and level < 30


def sun_target(level):
    from .config import SUN_TARGET_DEFICIENT, SUN_TARGET_NORMAL

    return SUN_TARGET_DEFICIENT if is_deficient(level) else SUN_TARGET_NORMAL


def supp_target(level):
    from .config import SUPP_TARGET_DEFICIENT, SUPP_TARGET_NORMAL

    return SUPP_TARGET_DEFICIENT if is_deficient(level) else SUPP_TARGET_NORMAL
