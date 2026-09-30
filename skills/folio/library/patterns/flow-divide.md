---
id: flow-divide
family: device
registers: [magazine, book, corporate]
loud: false
seen_in: ["user rule 2026-09-29: the two-page colour area should meet with a flowing edge instead of a straight divide"]
---
# Flow divide

**Why it works:** A colour area that spans a spread and ends in a slow wave feels drawn, not ruled; the eye follows it across the fold. A straight edge reads as a template band.

**Rules**
- Draw the field as one SVG (`imagery.py divide --w <spread mm> --h <band mm> --edge top|bottom --color <hex>`) placed as a `.cross` element on both pages.
- One gentle wave (amplitude 4–8% of the band height, one or two crests across the spread); never ripples.
- Text on the field keeps 6mm clear of the crest.
- Photos stay rectangles; the wave belongs to the colour field only.

**Goes generic when**
- Every page has a wave; waves under text; several colours stacked as bands.
