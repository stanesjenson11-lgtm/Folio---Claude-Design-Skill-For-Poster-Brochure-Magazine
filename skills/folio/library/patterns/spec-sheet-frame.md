---
id: spec-sheet-frame
family: data
registers: [catalog]
loud: false
seen_in: ["house-07 valve data sheet: title block, ballooned drawings, dimension table keyed to the drawing", "house-09 one-system-per-page spec sheets (label/value pairs + included list)"]
---
# Spec sheet frame

**Why it works:** An engineer files and cites a data sheet. Keeping engineering conventions (title block, drawing numbers, keyed dimensions) makes the page trustworthy; design adds hierarchy, not decoration.

**Anatomy**
```
┌─┬─────────────────────────────────┐
│D│ Wordmark   PRODUCT  variant     │  header
│W│ size · DWG no · rev · date · by │  title-block strip
│G├──────────────────┬──────────────┤
│ │ 01 DIMENSIONS    │ sectional    │  60 / 40 split
│c│ size × D1 D2 H1  │ view ①–⑱     │  left: numbered data sections
│o│ 02 MATERIALS     ├──────────────┤  right: drawings on a 5mm grid
│d│ items 1–9│10–18  │ assembly     │  with dark title bar + sheet code
│e│ 03 SPEC  04 FEAT │ [150] [222]  │  rating tiles repeat key limits
├─┴──────────────────┴──────────────┤
│ company · product · DWG no        │  footer
└───────────────────────────────────┘
```

**Rules**
- Keep the client's vector drawings. Balloon numbers match item numbers in the materials table; dimension letters match the table's column heads.
- Size-matrix table: sizes as rows, dimensions as columns, grouped headers, one tinted governing column, right-aligned tabular figures, units stated once under the table.
- A long bill of materials splits into two side-by-side tables.
- For services or systems (one per page): label/value pairs on hairlines + an "Included" list + one photo; alternate the photo side or scale every two pages so eight sheets in a row don't look stamped.
- Type floor 6.5pt even here; if it doesn't fit, it becomes two pages.
- The document code repeats in the footer (optionally on a vertical spine).

**Goes generic when**
- Rounded cards, tick icons and alert widgets (a web UI, not an engineering sheet).
- The same data given twice (table and cards).

**Build notes:** A4 portrait, one `.page`; drawings as SVG; `vertical-title` for the spine code.
