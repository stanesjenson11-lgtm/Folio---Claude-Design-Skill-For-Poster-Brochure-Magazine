---
id: mosaic
family: gallery
registers: [corporate, catalog, magazine]
loud: false
seen_in: ["ref-01 learning & faculty grid", "ref-03 pipe plugging photo grid", "ref-07 content page thumbnails"]
---
# Mosaic gallery

**Why it works:** Event or product photos packed into a tight grid with narrow gutters (1–2mm), one tile larger than the rest. Many modest photos become one strong image.

**Anatomy**
```
┌─────────────────────┐
│ Learning &   ▭ ▭ ▭  │   gutters 1–2mm, all tiles on grid
│ Faculty      ▭ ███  │   one hero tile 2×2
│ ≈≈≈≈≈        ▭ ███  │   captions in a column, not under
│ ≈≈≈≈≈   ▭ ▭ ▭ ▭ ▭  │   every tile
└─────────────────────┘
```

**Rules**
- Same colour treatment for all tiles (grade them together).
- Tiles align to the page grid; the mosaic bleeds off one edge.
- Weak/low-res photos go in the smallest tiles.

**Goes generic when**
- Photos with white frames, rounded corners and shadows (polaroid clutter).
- Every tile a different size.

**Build notes:** CSS grid inside a `.box` with `gap:1.5mm`; each tile a `.ph` with focal points.
