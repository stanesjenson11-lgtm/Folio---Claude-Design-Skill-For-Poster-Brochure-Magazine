---
id: stat-spread
family: data
registers: [corporate, catalog]
loud: true
seen_in: ["ref-01 performance page (110 / 98 / 40 circles)", "ref-04 profit structure donuts 50/35/15", "ref-04 back-of-book 85+ 92% 70% 28%"]
---
# Stat spread

**Why it works:** Three to five key numbers set as giant numerals or as circles sized by their value. Readers remember numbers they can see from across the room.

**Anatomy**
```
┌─────────────────────┐
│ Performance         │
│   ◯110   ◯98        │   circles sized ∝ value (area!)
│ ◯40     70%  GPA    │   or numerals 40–90pt in brand
│  248 TOTAL          │   label 7.5–8.5pt beneath
│ small table / notes │
└─────────────────────┘
```

**Rules**
- Every number has a label and a period/source; no invented stats.
- If circles encode values, scale their AREA, not diameter, to the value.
- Numerals use tabular lining figures in the display face.
- One accent for the hero number, brand colour for the rest.

**Goes generic when**
- Hero-metric SaaS cliché: big number, small label, gradient, repeated in identical cards.
- Numbers without units or year.

**Build notes:** Numerals `.stat-n` style; circles as SVG with `r = sqrt(value/max) * Rmax`.
