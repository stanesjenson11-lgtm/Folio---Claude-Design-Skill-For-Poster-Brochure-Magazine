---
id: skate-culture
name: Skate Culture
family: sport & action
size: A4 (210 x 297 mm)
pages: 8
render: --bleed 3
fonts: Barlow Condensed:500,600,700,800; Barlow:700,800,800i; Sedgwick Ave Display:400; Familjen Grotesk:400,600,700
theme: brand #C8DD4A; accent #E2493C
---
# Skate Culture

**Looks like:** A street-culture magazine: a sky-blue photo cover with a huge condensed lime masthead that switches case mid-word (MANGOinc, SKATEboard), a cut-out person jumping in front of it, lime cover lines, a black circle badge, an extended bold italic word, a tilted lime tape with a tagline and a big white graffiti word; inside, black spreads with graffiti chapter titles, a red light-trail hero crossing the fold, a lime coverage box, a word repeated in red graffiti behind a framed photo, a white contents column, a red text panel with a white "Spotlight" column, and a black-and-white back cover. User reference 1:1.

**Page archetypes:** 1 cover · 2–3 chapter spread (black page, graffiti title, two text columns, small photo; hero photo across the fold; white panel with text + photo; lime coverage box with a thumbnail) · 4–5 word repeated in red behind a framed photo; half-page portrait + white contents column + black box · 6–7 photo, red two-column panel, white spotlight column, bottom photo; black page with graffiti title, lime note, two thumbnails with notes, big black-and-white photo · 8 black-and-white back cover with the logo and barcode

**Image slots:** a cut-out person in motion (`imagery.py cutout --person`) over a sky photo graded blue (`imagery.py grade --treatment duotone --ink #0B1730 --brand #2F5CA8 --paper #A9C6F2`); a light-trail or neon action photo for the hero; black-and-white shots (`imagery.py grade --treatment bw`) for page 7 and the back; the barcode regenerates in ink

**Theme colours:** brand #C8DD4A (lime); accent #E2493C (red).

**Deviations from the reference:** the lime logo on white is deepened to #869A10 for print contrast; the pull quote on red is 14pt bold so white passes

**Using it:** follow `reference/kit-flow.md` (`/folio:skate`). Fill every `data-kit-sample` element with the client's content, make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings.
