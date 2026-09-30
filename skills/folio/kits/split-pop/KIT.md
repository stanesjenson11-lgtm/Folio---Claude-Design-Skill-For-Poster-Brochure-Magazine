---
id: split-pop
name: Split Pop (Portfolios)
family: pop & colour
size: 16:9 (320 x 180 mm)
pages: 10
render: --single
fonts: Familjen Grotesk:400,600,700; Bodoni Moda:700
theme: brand #0FA5A1; accent #F26A00
---
# Split Pop (Portfolios)

**Looks like:** Landscape portfolio pages cut into hard colour splits: a narrow side rail with the page number, year and a two-bar mark, a big teal or orange field, white reading panels. Titles in heavy caps with a colour disc behind the first letter; hatched circles, brackets and half-discs; objects on one colour; phone, tablet and desktop mockups of the client's own screens. Loud, clean, commercial. User-loved (1:1 replica of their 'Portfolios' reference).

**Page archetypes:** 1 cover (white rail, teal field, orange hero disc with a cut-out object) · 2 services (orange panel + tall photo, teal field with three photos and two text columns) · 3 delivery (photo grid, two icon bullets, teal strip) · 4 feature (teal text panel, orange field with a cut-out hero, small photo, hatched square, dot) · 5 projects (tall photo, two photo columns under a title) · 6 mobile (phone mockup, two text blocks, split strip) · 7 design (tall photo under the title, 2 x 2 grid) · 8 cloud (photo row + wide photo on orange, text on teal, hatched half-disc) · 9 websites (desktop mockup, icon bullet) · 10 contact (tablet mockup, contacts, credits)

**Image slots:** objects on the accent colour (duotone ink → accent → light: `imagery.py grade --treatment duotone --brand <accent>`); two cut-outs (`imagery.py cutout`) for the hero disc and the feature field; device mockups (`imagery.py screenshot` + `mockup`) of the client's site; hatches regenerate with `imagery.py hatch` in the new colours

**Theme colours:** brand #0FA5A1; accent #F26A00 (swapped by `kit.py new --brand/--accent`; variants keep their lightness offset).

**Deviations from the reference:** no thin line after titles (user bans decorative rules); fields deepened so white titles reach 3:1; small text on fields in ink

**Using it:** `kit.py new split-pop <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe below, keep the page roles, then `render.py <file>.html --single` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count; keep the rhythm (loud / quiet) and the continuity devices.
