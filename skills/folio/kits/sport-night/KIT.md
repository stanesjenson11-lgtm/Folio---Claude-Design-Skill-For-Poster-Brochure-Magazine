---
id: sport-night
name: Sport Layers Night
family: sport & action
best_for: tech, gaming, sport, launches, events; dark and high-energy; one cut-out person (4000 px+ source), a hero device or object, 8+ photos; 12 pages
size: A4 (210 x 297 mm)
pages: 12
render: --bleed 3
fonts: Big Shoulders Display:800,900; Familjen Grotesk:400,500,600,700
theme: brand #2F5BEA; brand-2 #3D7BFF; accent #FF6A1A; accent-2 #FFB38A
---
# Sport Layers Night

**Looks like:** A dark, high-contrast sports-magazine for any subject: near-black grounds with a faint duotone photo shared across each spread, electric blue note boxes that run from the left page to the right, blaze-orange numbers and vertical words, one light page for contrast. The cover stacks a context background, a glow, a newsprint overlay, the masthead, a motion streak, a cut-out person, a flying hero object and a spark. Bold words both horizontal and vertical (top to bottom). User-loved.

**Page archetypes:** 1 layered cover · 2–3 contents with a vertical word + studio intro, gutter box · 4–5 big word + layered photo and device, services with real logos, a flowing band across the spread · 6–7 dark opener with a vertical word + a light stack page with logos, gutter box · 8–9 two big words, layered photos, a cut-out object crossing the fold, a light panel with a flowing edge · 10–11 a giant numeral + stars, price, a flowing band with steps, directors with circle placeholders, gutter box · 12 back (cut-out, sign-off, contacts)

**Image slots:** context grounds (`imagery.py grade --treatment duotone --ink #05070D --brand <brand-mid> --paper <light>`); one cut-out person (`imagery.py cutout --person`, ≥ 4000 px source); a hero object (the client's own screen in a mockup, rotation baked into the file); cut-out objects; technology logos (`imagery.py logos … --color #F2F4F8`, ink versions for the light page); streak, spark, newsprint, bands regenerate in the new colours

**Theme colours:** brand #2F5BEA; brand-2 #3D7BFF; accent #FF6A1A; accent-2 #FFB38A (swapped by `kit.py new --brand/--accent`; variants keep their lightness offset).

**Deviations from the reference:** —

**Using it:** `kit.py new sport-night <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe below, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count; keep the rhythm (loud / quiet) and the continuity devices.
