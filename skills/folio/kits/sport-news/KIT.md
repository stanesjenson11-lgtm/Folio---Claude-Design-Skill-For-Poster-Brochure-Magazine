---
id: sport-news
name: Sport News
family: sport & action
size: A4 (210 x 297 mm)
pages: 14
render: --bleed 3
fonts: Russo One:400; Bruno Ace SC:400; Familjen Grotesk:400,600,700
theme: brand #F7E600; accent #11101E
---
# Sport News

**Looks like:** A punchy news-style sports magazine: a full-bleed dramatic photo cover in navy with an acid-yellow masthead, yellow-triangle cover lines, a barcode and a vertical strip (yellow blocks, a white box with a big number and vertical words); inside, heavy small caps (Russo One with font-variant-caps: small-caps), full yellow contents panel with numbered photo items, yellow title and bullet boxes beside glowing photos, a yellow vertical title box, a full dark hero page and a toned back cover with a big headline. User reference 1:1.

**Page archetypes:** 1 cover (dim photo, brand + barcode, four triangle cover lines, vertical strip with two-line words and a big number, huge masthead word + NEWS + Magazine) · 2–3 contents (yellow panel, four numbered photo items; two photos with items 05/06, big photo) · 4–5 feature (heavy small-caps title, two-column paragraph, yellow bullet box + glowing photo; bullet + small photo, hero) · 6–7 yellow sidebar with vertical title and text + tall photo and bullets; three stacked photos with bullets, yellow edge tabs, yellow text box · 8–9 full dark photo with white headline and bullets; yellow panel with title + paragraph over a photo · 10–11 yellow vertical title box, photo, bullets, paragraph + small photo; full dark hero · 12–13 toned photo with big headline; title + two columns with a yellow bar, wide photo, bullets, yellow box · 14 back cover (masthead, contacts, directors with circle placeholders)

**Image slots:** dramatic, dark, on-topic people shots (gamers, developers, people with VR or headphones in hard light), 3200 px+; the back cover photo toned with `imagery.py grade --treatment duotone --ink #11101E --paper <brand>`; barcode and triangle bullets regenerate in the brand colour

**Theme colours:** brand #F7E600; accent #11101E.

**Deviations from the reference:** no thin rules; vertical words read top to bottom

**Using it:** `kit.py new sport-news <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count.
