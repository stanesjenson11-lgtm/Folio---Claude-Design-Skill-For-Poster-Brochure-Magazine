---
id: data-tint
family: data
registers: [corporate, catalog]
loud: false
seen_in: ["ref-04 geographic reach + product distribution table", "ref-02 raised sales charts"]
---
# Data on tint

**Why it works:** Tables and charts sit on a brand-tint panel or a brand band, drawn only in brand colour + one neutral. The tint separates data from narrative and one colour makes five charts look like a family.

**Anatomy**
```
┌───────┬─────────────┐
│ tint  │ GEOGRAPHIC  │   left: tint column with
│ donut │ REACH       │   donuts/bars stacked
│ 50%   │ table: rule │   right: table with header rule
│ donut │ ─────────── │   bottom: brand band with a
│ 35%   │█ line chart█│   line chart in white
└───────┴─────────────┘
```

**Rules**
- One chart type per kind of data across the whole book.
- Chart colours: brand, brand at 40%, neutral. No rainbow.
- Tables: header rule 0.8pt, row hairlines 0.25pt, right-aligned tabular figures, no vertical lines.

**Goes generic when**
- Default chart-library styling (grid lines, legends in boxes, 6 colours).
- Tables with every border drawn.

**Build notes:** Hand-built SVG charts (exact control, print-crisp) with `vector-effect: non-scaling-stroke`; tables styled by folio.css.
