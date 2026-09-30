---
id: vertical-title
family: device
registers: [corporate, catalog, magazine]
loud: true
seen_in: ["ref-02 CONTENT spine title, HEADLINE HERE", "ref-07 YOUR FIGHT TRAINS / SPEED WANT A BRAVERY", "ref-05 WELCOME"]
---
# Vertical title

**Labels, section tabs and spine titles only — never the main headline** (user taste: rotated headlines are hard to read; preflight `rotated-heading`).

**Why it works:** Setting a heading vertically along the spine or outer edge frees the page's width for photos and adds a strong architectural line.

**Anatomy**
```
┌──┬──────────────────┐
│C │░░░ PHOTO ░░░░░░░ │   vertical title reads bottom→top,
│O │░░░░░░░░░░░░░░░░░ │   runs 60–90% of page height,
│N │ text…            │   heavy condensed caps
│T │                  │
└──┴──────────────────┘
```

**Rules**
- Reads bottom-to-top (rotated −90°) for left-side titles.
- Only one vertical title per spread.
- Keep ≥ 9mm from the spine if placed there.

**Goes generic when**
- Vertical text for body copy.
- Several vertical labels competing.

**Build notes:** `.vert` class (writing-mode + rotate) inside a `.box`; size by height.
