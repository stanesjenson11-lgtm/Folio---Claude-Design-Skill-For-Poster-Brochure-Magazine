---
id: slab-cover
family: cover
registers: [corporate, catalog]
loud: true
seen_in: ["ref-02 corporate report (cover)"]
---
# Slab cover

**Why it works:** Vertical brand slabs anchored to the top and bottom edges frame a very heavy condensed title and a single dramatic photo band. The geometry is architectural and the white space is deliberate, which reads corporate without being dull.

**Anatomy**
```
┌─────────────────────┐
│              ┌────┐ │   slab: brand colour, top edge bleed,
│ Annual Tmpl  │logo│ │   holds the logo
│ REPORT       │    │ │   title: condensed 800–900 weight
│              └────┘ │
│█████ PHOTO ████████ │   photo band bleeds left, 35–40% height
│█████████████████████│
│ small copy     2020 │
│             ┌────┐  │   small slab echoes the top one
└─────────────┴────┴──┘
```

**Rules**
- Slabs are the same width and align to one grid column edge.
- Photo band bleeds off the left (or both) edges; nothing else bleeds.
- Year set as display numerals at the bottom right, aligned to the slab.

**Goes generic when**
- Slabs of random widths.
- Photo boxed with margins on all sides.

**Build notes:** Two `.box` slabs with `top: var(--b0)` / `bottom: var(--b0)`; photo `.ph` with `left: var(--b0)`.
