---
id: offset-block
family: text
registers: [corporate, catalog]
loud: false
seen_in: ["ref-05 agriculture brochure (cover + interiors)"]
---
# Offset block

**Why it works:** A photo overlaps a solid colour block that is shifted a few millimetres off its corner. The layering gives flat pages depth and a signature device you can repeat on every page.

**Anatomy**
```
┌─────────────────────┐
│ ABOUT         ┌───┐ │
│ AGRICULTURE ┌─┴─┐ │ │   colour block offset 6–12mm
│ ≈≈≈≈≈≈≈     │PH │▓│ │   down-right (or up-left)
│ ≈≈≈≈≈≈≈     │   │▓│ │
│             └───┘─┘ │
└─────────────────────┘
```

**Rules**
- Offset direction and distance are identical everywhere in the book.
- Block colour is the brand colour; the photo has no border or shadow — the block IS the shadow.

**Goes generic when**
- Mixed with drop shadows.
- Offset varies page to page.

**Build notes:** Two `.box` elements: block `inset` = photo `inset` shifted by `--offset: 8mm`.
