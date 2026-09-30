---
id: cutout-layers
family: cover
registers: [magazine]
loud: true
seen_in: ["ref-11 sport news magazine", "ref-13 football magazine", "ref-15 skateboard magazine", "user brief 2026-09-29: shaded background, a person popping out, layered images"]
---
# Cut-out layers

**Why it works:** Depth sells energy. A faint shaded photo in the ground, one colour field, a person cut out and breaking out of the frame (over the masthead or a panel edge), and one or two photos offset in front and behind make the page feel physical, like stacked prints, rather than a grid.

**Anatomy (back to front)** (for magazines use the full stack in `sport-layers`: context ground, masthead, person, hero object, motion streak, spark, newsprint overlay)
1. Ground colour + a low-opacity shaded photo (12–25%, duotone-graded into the ground, marked `data-texture`) + grain.
2. One colour field (palette support or accent).
3. A rectangular photo offset behind the figure.
4. The cut-out person (`imagery.py cutout photo.jpg --person`), standing on the page foot or a panel, overlapping the masthead or the field's edge.
5. A second small photo or sketch in front, overlapping the figure's side.
6. Type: the masthead or headline behind the head, cover lines and numbers in front.

**Rules**
- Depth from overlap and z-order only; never drop shadows.
- The face stays clear of type.
- Stock people are illustrative: never captioned as the client's team; credit the photographer.

**Build notes:** z-index layers in CSS (the editable export keeps the order); duotone the ground photo with `imagery.py grade --treatment duotone`, not CSS filters (Canva drops filters).
