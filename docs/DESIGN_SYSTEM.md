# vitd Design System

Design tokens, components, and patterns for the vitd PWA.

---

## Color Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#0a0a0c` | Page background |
| `--surface` | `#141418` | Cards, panels |
| `--elevated` | `#1e1e24` | Inputs, buttons, hover states |
| `--border` | `#2a2a32` | Borders, dividers |
| `--fg` | `#f5f5f7` | Primary text |
| `--muted` | `#6e6e7a` | Secondary text, labels |
| `--subtle` | `#3a3a44` | Tertiary accents |
| `--accent` | `#4ade80` | Success, primary action, normal levels |
| `--accent-glow` | `rgba(74,222,128,.15)` | Shadows, glows behind accent elements |
| `--sun` | `#f59e0b` | Sun-related metrics |
| `--sun-glow` | `rgba(245,158,11,.15)` | Sun card/button glows |
| `--supp` | `#3b82f6` | Supplement-related metrics |
| `--supp-glow` | `rgba(59,130,246,.15)` | Supplement card/button glows |
| `--alert` | `#ef4444` | Errors, severe deficiency |
| `--alert-glow` | `rgba(239,68,68,.15)` | Danger glows |
| `--warn` | `#f59e0b` | Warnings, deficient/insufficient |
| `--warn-glow` | `rgba(245,158,11,.15)` | Warning glows |

### Status Color Mapping

| Level Range | Color | Glow |
|-------------|-------|------|
| Severe (<10) | `--alert` | `--alert-glow` |
| Deficient (<20) | `--warn` | `--warn-glow` |
| Insufficient (<30) | `#fcd34d` | `--warn-glow` |
| Normal/Sufficient (30+) | `--accent` | `--accent-glow` |

---

## Typography

| Style | Size | Weight | Tracking | Usage |
|-------|------|--------|----------|-------|
| Logo | 22px | 800 | -0.8px | App header |
| Hero Level | 42px | 800 | -2px | Big number in hero |
| Section Title | 12px | 700 | 1px | Card section headers |
| Stat Value | 22px | 800 | -0.5px | Key metric numbers |
| Stat Label | 11px | 700 | 0.8px | Metric labels |
| Body | 14px | 400 | 0 | Tips, descriptions |
| Body Muted | 14px | 400 | 0 | Secondary descriptions |
| Button | 14-15px | 700 | 0 | Actions |
| Small | 11-12px | 600 | 0.5px | Hints, metadata |

---

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Inline gaps, tight padding |
| sm | 8px | Component internal gaps |
| md | 10-12px | Card padding, grid gaps |
| lg | 14-16px | Section margins |
| xl | 20-24px | Card border-radius, section spacing |
| 2xl | 28px | Bottom sheet padding |

---

## Shadows

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,.3)` | Subtle elevation |
| `--shadow` | `0 4px 12px rgba(0,0,0,.4)` | Cards, FAB |
| `--shadow-lg` | `0 8px 30px rgba(0,0,0,.5)` | Modals, toasts |

---

## Border Radius Scale

| Token | Value | Usage |
|-------|-------|-------|
| sm | 8-10px | Small buttons, badges |
| md | 12-14px | Buttons, nav items |
| lg | 16px | History items, small cards |
| xl | 20px | Cards, tip cards, settings groups |
| 2xl | 24px | Hero card, bottom sheet, confirm dialog |
| full | 50% | Circular buttons, dots, rings |

---

## Components

### Hero Card
- Background: gradient from `--surface` to `--elevated`
- Border: `1px solid --border`
- Radius: 24px
- Padding: 24px
- Glow: radial gradient in top-right corner using status color glow
- **Urgent variant**: red glow for severe/deficient

**Structure:**
```
Hero Card
├── Top Row (flex, space-between)
│   ├── Label: "Vitamin D Level" (11px uppercase)
│   └── Status Badge (pill, color-coded)
├── Main Row (flex, gap 20px)
│   ├── Ring (110px SVG, animated stroke-dashoffset)
│   └── Info
│       ├── Level (42px, color-coded)
│       ├── ETA text (13px muted)
│       └── Target Bar (flex, gap 8px)
│           ├── Bar (flex-1, 6px height, rounded)
│           └── Percent text (11px)
```

### Stat Card
- Background: `--surface`
- Border: `1px solid --border`
- Radius: 20px
- Padding: 18px 16px
- Top accent bar: 3px height, color matches type (sun/supp/test/note)
- Hover: `translateY(-1px)`, border lightens
- Active: `scale(0.98)`

**Structure:**
```
Stat Card
├── Top Accent Bar (3px, type color)
├── Icon (24px)
├── Label (11px uppercase muted)
├── Value (22px, type color)
└── Subtext (11px muted, contextual)
```

### History Item
- Background: `--surface`
- Border: `1px solid --border`
- Radius: 16px
- Padding: 14px 16px
- Layout: flex row, gap 14px

**Structure:**
```
History Item
├── Date Column (48px, center)
│   ├── Day name (10px uppercase muted)
│   └── Date number (22px bold)
├── Content (flex-1, column)
│   ├── Row: dot + "Sun" label + value
│   ├── Row: dot + "Supp" label + value
│   └── Optional note (12px muted)
└── Indicator Dot (8px, color-coded)
```

### Timeline Item
- Connected by vertical line (2px, `--subtle` gradient)
- Dot: 12px circle with 3px `--bg` border
- Content card: `--surface`, 14px radius

**Structure:**
```
Timeline Item (flex, gap 14px)
├── Dot (12px, z-index 1, color-coded, glow shadow)
└── Content Card
    ├── Date (11px muted)
    ├── Level (18px bold, color-coded)
    └── Badge (pill, color-coded)
```

### Tip Card
- Background: `--surface`
- Border: `1px solid --border`
- Radius: 20px
- Padding: 18px 16px
- **Critical variant**: red border + gradient background

**Structure:**
```
Tip Card
├── Header (flex, gap 10px)
│   ├── Icon Box (36px square, 12px radius, --elevated)
│   └── Title (15px bold)
└── Content (14px, muted, strong in --fg)
```

### Settings Row
- Background: transparent (inherits group)
- Border-bottom: `1px solid --border`
- Padding: 14px 16px
- Hover: `rgba(255,255,255,.02)`
- Active: `rgba(255,255,255,.04)`

**Structure:**
```
Settings Row (flex, space-between, gap 12px)
├── Info (flex-1)
│   ├── Label (14px semibold)
│   └── Desc (12px muted)
└── Action Icon (20px, muted)
```

### Bottom Sheet
- Background: `--surface`
- Border-top: `1px solid --border`
- Radius: 24px top
- Padding: 20px 20px 28px
- Transform: `translateY(100%)` → `translateY(0)`
- Transition: `0.4s cubic-bezier(.32,.72,0,1)`

**Structure:**
```
Sheet
├── Handle (36x4px, --subtle, centered)
├── Title (18px bold)
├── Input (28px bold, centered, --elevated bg)
├── Hint (12px muted, centered)
└── Actions (grid, 1fr 1.5fr)
    ├── Cancel button
    └── Save button (--accent)
```

### Toast
- Background: `--elevated`
- Border: `1px solid --border`
- Radius: 14px
- Padding: 12px 20px
- Transform: `translateY(20px) scale(0.95)` → `translateY(0) scale(1)`
- Transition: `0.4s cubic-bezier(.32,.72,0,1)`

**Structure:**
```
Toast (inline-flex, gap 10px)
├── Optional Icon (16px)
├── Message (13px semibold)
└── Optional Action Button
```

### FAB (Floating Action Button)
- Size: 56px circle
- Background: `--accent`
- Shadow: `0 4px 16px var(--accent-glow)`
- Icon: `+` (rotates 45deg when open)

**Options (expanded):**
- 44px circles, color-coded by type
- Labels: 12px pill on left side
- Staggered appearance on open

---

## Animation Patterns

### Easing Tokens

| Name | Value | Usage |
|------|-------|-------|
| `ease-spring` | `cubic-bezier(.32,.72,0,1)` | Default for all transitions |
| `ease-out` | `cubic-bezier(0,0,.2,1)` | Subtle movements |

### Animation Presets

| Name | Duration | Effect |
|------|----------|--------|
| `reveal` | 0.4-0.5s | `opacity: 0→1`, `translateY(16px→0)` |
| `count-up` | 0.4-0.6s | Number interpolation with ease-out-cubic |
| `ring-fill` | 1s | `stroke-dashoffset` with spring easing |
| `shake` | 0.4s | `translateX` oscillation |
| `pop` | 0.25s | `scale(1→1.15→1)` |
| `float` | 3s infinite | `translateY(0→-8px→0)` ease-in-out |
| `skeleton` | 1.5s infinite | Background gradient sweep |

### Stagger Rules
- List items: 40-60ms delay per item, max 400-600ms
- FAB options: 50ms sequential delay
- Tip cards: 60ms delay

---

## Layout Patterns

### App Shell
```
App (max-width: 480px, centered)
├── Header (fixed height, gradient bg)
├── Main (flex:1, overflow hidden)
│   └── Panels (flex row, transform translateX)
│       ├── Today Panel
│       ├── History Panel
│       ├── Tips Panel
│       └── Settings Panel
├── Bottom Nav (fixed, gradient bg)
└── FAB (fixed, bottom-right)
```

### Panel Scroll
- `overflow-y: auto`
- `-webkit-overflow-scrolling: touch`
- Bottom padding: 80px (clear FAB + nav)
- Hide scrollbar: `::-webkit-scrollbar { width: 0 }`

---

## Accessibility

- All interactive elements are `<button>` with `aria-label`
- Decorative icons have `aria-hidden="true"`
- Nav uses `role="tablist"` / `role="tab"` / `aria-selected`
- Modal uses `role="dialog"` / `aria-modal="true"`
- Screen reader live region: `#srLive`
- `prefers-reduced-motion`: disable all animations (set duration to 0.01ms)
- `focus-visible` outlines: 2px solid `--accent`

---

## Z-Index Scale

| Layer | Z-Index | Element |
|-------|---------|---------|
| Base | 1 | Content |
| Header | 10 | App header |
| FAB | 50 | Floating button |
| Backdrop | 99 | Modal backdrop |
| Sheet | 101 | Bottom sheet |
| Confirm | 150 | Confirm dialog |
| Toast | 200 | Toast container |

---

## Responsive Behavior

The app is mobile-first with a fixed max-width of 480px. On larger screens:
- Centered container
- All internal spacing remains consistent
- No layout changes — the app maintains its phone-like experience

---

## File Location

This design system documents the current state of:
- `docs/index.html` — the single-file PWA
- `docs/manifest.json` — PWA manifest
- `docs/sw.js` — service worker

Last updated: 2026-04-22
