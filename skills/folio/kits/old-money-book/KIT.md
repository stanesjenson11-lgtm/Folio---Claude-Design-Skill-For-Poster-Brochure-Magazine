---
id: old-money-book
name: Old-money Classic Book
family: editorial & minimal
best_for: company profiles, law, finance, real estate, schools, heritage brands; quiet and expensive; few photos (they become pencil sketches), portrait placeholders; 8 pages
size: A4 (210 x 297 mm)
pages: 8
render: --bleed 3
fonts: Bodoni Moda:400,400i,500; Familjen Grotesk:400,600
theme: brand #7D8B6A; accent #C9A96E
---
# Old-money Classic Book

**Looks like:** A quiet, expensive company book: ivory paper, espresso type, a champagne seal, sage heads and bands that meet with a flowing edge across the services spread, coloured-pencil sketches beside the text, portrait placeholders on the people page, and a back page where an ivory sign-off meets an espresso contact field with a flowing edge. Sharp editorial serif throughout. User-loved as a book style.

**Page archetypes:** 1 cover (masthead, italic line, seal, large sketch) · 2 contents (sketch) · 3 studio (sage head with a quote, stat, text) · 4–5 services spread (Build / Design / Media with sketches, a sketch across the fold, a flowing sage band with timelines) · 6 print work (sketch + champagne field) · 7 people (sage head, two portrait placeholders, promise line) · 8 back (sign-off + sketch over an espresso field with a flowing edge, contacts)

**Image slots:** coloured-pencil sketches of on-topic photos (`imagery.py sketch`); flowing bands (`imagery.py divide --edge both|top`); portrait placeholders stay until the client sends photos; paper texture regenerates from textures.txt

**Theme colours:** brand #7D8B6A; accent #C9A96E (swapped by `kit.py new --brand/--accent`; variants keep their lightness offset).

**Deviations from the reference:** —

**Using it:** `kit.py new old-money-book <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe below, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count; keep the rhythm (loud / quiet) and the continuity devices.
