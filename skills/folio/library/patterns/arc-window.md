---
id: arc-window
family: cover
registers: [corporate, catalog]
loud: true
seen_in: ["ref-01 school annual report (cover + back cover)"]
---
# Arc window

**Why it works:** A brand-colour circle far larger than the page, cropped by two page edges, turns into a window or horizon rather than a sticker. The photo shows through the rest of the page, so the cover is half image, half colour field — institutional but not stiff.

**Anatomy**
```
┌─────────────────────┐
│ logo      ████████▓▓│   circle Ø 1.1–1.3 × page width,
│        ███████████▓▓│   centre off-page (top-right or right)
│  2032 ████████████▓▓│   title set ON the colour field
│  Annual Report ████▓│
│  deck line  ███████ │
│ ░░ PHOTO ░░░░ ▓▓▓▓  │   photo full-bleed underneath
│ ░░░░░░░░░░░░░░░░░░░ │
├─────────────────────┤   white base band 18–24mm:
│ phone   email   web │   contacts, brand rule on top edge
└─────────────────────┘
```

**Rules**
- Circle diameter ≥ 1.1× page width; its centre sits outside the trim so only an arc is visible.
- Title and deck sit fully on the colour field with ≥ 8mm clearance from the arc edge.
- Photo is architectural or landscape with a clear horizon; the arc should echo or cut across it, not cover faces.
- Reuse the arc on the back cover (as a mask on a second photo), section openers and portrait masks — it is the book's motif.
- Weight contrast in the title: light year + heavy word, or the reverse.

**Goes generic when**
- The circle floats fully inside the page like a badge.
- A second, unrelated shape language appears inside (rounded cards, waves).

**Build notes:** `.fill` photo + `.box` with `border-radius:50%; width:250mm; height:250mm; right:-95mm; top:-70mm`; or `clip-path: circle()` on a brand layer. Base band: `.box` bottom 0, height 22mm, white, with a 1.2mm brand bar on 60% of its top edge.
