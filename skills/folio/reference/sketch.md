# sketch — reading pencil and paper layouts

Users often photograph a hand-drawn page plan. Treat it as the art director's intent for structure and hierarchy, not as final geometry.

## Conventions (ask if a sketch uses its own)
| Mark | Meaning |
|---|---|
| box with an X or diagonal hatching | photo frame; extended to the paper edge = bleed |
| circle / arc with an X | masked (circular) photo |
| solid scribble-filled area | colour field / brand panel |
| thick short strokes, or big lettering | headline / display type (bigger strokes = bigger type) |
| parallel thin lines or wavy lines | running text; count lines to estimate length, column breaks = columns |
| small line under a box | caption |
| numbers in circles, "01" | numbered sequence / contents |
| arrows | reading order or "this crosses to the facing page" |
| two rectangles side by side | a spread (left = verso, right = recto) |
| words written in the box ("logo", "map", "chart") | literal content type |

## Procedure
1. Straighten mentally: identify the page outline, then measure every element as a fraction of page width/height.
2. Snap each fraction to the 12-column grid and the 16-row grid (`folio.css`). Record it as `grid-column / grid-row`, or for bleed elements as `inset` with `var(--b0)` on touching edges.
3. Write a layout spec per page and echo it back as an ASCII wireframe before building:

```
p4 (verso)                     spec
┌───────────────────────┐      photo  inset: b0 b0 45% b0     (bleeds top/left/right)
│█████████ PHOTO ███████│      h2     col 1/9  row 9/11       display 40pt
│███████████████████████│      body   col 1/7  row 11/16      2 cols? no → 1 col, 6 span
│ HEADLINE ─────        │      stat   col 8/13 row 11/14      numeral 60pt brand
│ ≈≈≈≈≈≈   ⑫           │
│ ≈≈≈≈≈≈   ≈≈≈          │
└───────────────────────┘
```
4. Where the sketch is ambiguous (is that a photo or a colour block?), ask once for all ambiguities together. Where it is physically impossible (text in the spine, a photo too small for its frame), say so and propose the nearest fix.
5. Improve without changing intent: align edges the sketch nearly aligned, make near-equal sizes equal, strengthen contrast between the biggest and smallest elements.
