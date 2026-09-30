---
id: product-cell-grid
family: data
registers: [catalog]
loud: false
seen_in: ["house-06 amenities catalog: ruled cells with name / material / dimension / MOQ / price chip", "house-11 seafood grades on one backdrop under a Latin-name bar"]
---
# Product cell grid

**Why it works:** Buyers compare like with like. Identical cells on one baseline, each with the same micro-format, let the eye jump across products instead of re-reading every layout.

**Anatomy**
```
┌──────────┬──────────┬──────────┐   hairline cross-rules, no boxes
│ [image]  │ [image]  │ [image]  │   fixed image box, common baseline,
│ NAME     │ NAME     │ NAME     │   same backdrop and angle
│ Material │ Material │ Material │   key–value spec list, one unit style
│ Size     │ Size     │ Size     │
│ CODE-01  │ CODE-02  │ CODE-03  │   code in one format and position
│ MOQ ● PoR│          │          │   MOQ + price state
└──────────┴──────────┴──────────┘
```

**Rules**
- Grid by item count: 2×2, 3×2 or 3×3 per page; an odd item takes a wide cell, never a stagger.
- Every sellable line has a code in one format.
- Variants: one hero image plus a row of small swatches or thumbnails with their codes, not a repeated cell per colour.
- Grades or sizes in the trade's own language (e.g. Colossal / Jumbo / Backfin) under a bar naming the species or family.
- Prices: "Price on request" or a separate dated price list so the catalog doesn't go stale; printed prices carry validity and tax notes.
- Check units against product and MOQ (pairs vs pieces, mm vs cm, "02 mm" vs "2 mm").

**Goes generic when**
- Rounded shadow cards and a different photo angle in every cell.
- The grid logic changes from page to page.

**Build notes:** CSS grid inside `.live`; `border-top: .25pt solid var(--rule)` per row; `font-variant-numeric: tabular-nums`; spec labels in `--font-label`.
