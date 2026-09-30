---
id: minimal-ebook
name: Minimal E-book
family: editorial & minimal
best_for: guides, e-books, courses, personal brands, creative portfolios; minimal and airy; 6+ vivid or neon photos of people; 8 single pages
size: A4 (210 x 297 mm), single pages
pages: 8
render: --single
fonts: Bodoni Moda:400,500,600,700; Big Shoulders Display:700,800,900; Pinyon Script:400; Familjen Grotesk:400,600,700
theme: brand #D9480F
---
# Minimal E-book

**Looks like:** A minimal white e-book led by vivid neon photographs: an orange-toned cover with a script word over big serif caps ('studio E-BOOK'), WELCOME with a corner-frame accent and an outlined note box, chapter pages with huge condensed numerals in the accent colour, a heading that runs onto its photo, vertical serif headings, small bold grotesk labels and quiet body text, and a THANKS closing page. User reference 1:1.

**Page archetypes:** 1 cover (quote, orange photo block, created-by / year, script + E-BOOK) · 2 welcome (framed photo, WELCOME, caps lead, body, note box) · 3 chapter 01 (label, heading, numeral, photo, side column) · 4 heading over photo · 5 chapter 02 · 6 vertical heading + chapter 03 · 7 feature with a big photo · 8 thanks + contacts

**Image slots:** neon-lit portraits and on-topic objects (headphones, VR, phones, robots) in orange / pink / blue light; the cover and one feature toned orange (`imagery.py grade --treatment duotone --ink #A63300 --brand #FF7A1A --paper #FFE9CF`); photo-led palette (`<html data-palette-photos>`)

**Theme colours:** brand #D9480F.

**Deviations from the reference:** no heavy rules under headings; vertical heads read top to bottom; the numerals and frame take the accent colour so the piece shows three colours

**Using it:** `kit.py new minimal-ebook <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --single` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count.
