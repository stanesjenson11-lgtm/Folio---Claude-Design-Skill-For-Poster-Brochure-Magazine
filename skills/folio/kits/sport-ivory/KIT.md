---
id: sport-ivory
name: Sport Layers Ivory
family: sport & action
size: A4 (210 x 297 mm)
pages: 12
render: --bleed 3
fonts: Big Shoulders Display:800,900; Bodoni Moda:400,400i,500; Familjen Grotesk:400,600
theme: brand #7D8B6A; accent #C9A96E
---
# Sport Layers Ivory

**Looks like:** The user's 'PERFECT' magazine: an espresso cover with a faint shaded photo, a huge masthead behind a cut-out person, a sage panel and a small offset photo; ivory reading pages sharing a faint shaded photo across each spread; champagne note boxes that stretch from the left page to the right with a small photo on the far side; sage bands with big ivory numerals; coloured-pencil sketches across the fold; real technology logos; circle placeholders for people.

**Page archetypes:** 1 cover · 2–3 contents + studio (gutter box) · 4–5 big word, layered photos, services with logos, a sketch across the fold, sage timeline band · 6–7 dark opener + light stack/industries page (gutter box) · 8–9 two big words, sage field + photo, a sketch across the fold, print list · 10–11 giant numeral + stars, price, sage band with steps, directors with circle placeholders (gutter box) · 12 back

**Image slots:** shaded grounds (duotone into ink/champagne); one cut-out person; layered rectangular photos (tinted); coloured-pencil sketches (`imagery.py sketch --palette "#3B2A20,#7D8B6A,#C9A96E,#F6F1E7"`); technology logos in espresso; paper and grain regenerate from textures.txt

**Theme colours:** brand #7D8B6A; accent #C9A96E (swapped by `kit.py new --brand/--accent`; variants keep their lightness offset).

**Deviations from the reference:** —

**Using it:** `kit.py new sport-ivory <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe below, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count; keep the rhythm (loud / quiet) and the continuity devices.
