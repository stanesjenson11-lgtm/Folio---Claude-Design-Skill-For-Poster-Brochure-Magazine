---
id: layer-section
family: data
registers: [catalog, corporate]
loud: true
seen_in: ["house-10 exploded turf cross-section with callouts on both sides"]
---
# Layer section

**Why it works:** The parts a client pays for are often hidden (sub-base, drainage, insulation, laminate layers). An exploded cross-section with labelled layers makes the invisible work visible and justifies the price.

**Anatomy**
```
 label ····· ▭▭▭▭▭▭▭▭▭ ····· label     layers stacked with small gaps
 label ····· ▭▭▭▭▭▭▭▭▭ ····· label     dot-leader callouts on both flanks
 label ····· ▭▭▭▭▭▭▭▭▭ ····· label     material + thickness in each label
 ████ 10-YEAR MINIMUM TURF LIFE ████   accent bar with the key claim
```

**Rules**
- Each layer labelled with its material and thickness from the client's spec.
- Callouts alternate sides so labels don't crowd.
- One claim in the accent bar, and only if the client's spec supports it.

**Goes generic when**
- A stock 3D render with unlabelled layers.

**Build notes:** SVG layers (the editable export keeps them); `imagery.py prompt` can brief a textured version, labelled afterwards in HTML.
