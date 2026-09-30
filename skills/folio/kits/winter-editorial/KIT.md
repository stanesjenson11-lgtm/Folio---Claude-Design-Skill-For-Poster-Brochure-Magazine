---
id: winter-editorial
name: Winter Editorial
family: editorial & minimal
best_for: editorial, travel, fashion, architecture, premium company magazines; minimal and photo-led; 15+ strong photos including landscapes for full-bleed spreads; 20 pages
size: A4 (210 x 297 mm)
pages: 20
render: --bleed 3
fonts: Big Shoulders Display:700,800,900; Familjen Grotesk:400,500,600,700
theme: brand #111114; accent #2E5B8A
---
# Winter Editorial

**Looks like:** A minimal white editorial magazine: a cover with a heavy condensed black masthead ending in a full stop over a big cool-toned photo, tiny cover lines in the corners, a spaced MAGAZINE line and a barcode; inside, heavy condensed heads ending in a full stop, single drop-cap letters above narrow text columns, big photos and stacked photo columns, full-page photos with white titles, a panorama across a spread, a full-bleed spread photo, three-column grids with tall photo rows. Layered, never plain: a cool paper grain on every white page, ice-blue panels and bands, navy note boxes, faint background words, and on every spread a photo, box or band that crosses the fold. User reference 1:1.

**Page archetypes:** 1 cover · 2–3 contents with a photo column; letter from the studio with a photo rail · 4–5 big title, drop cap text, tall photo; text column and two stacked photos · 6–7 drop cap text and three stacked photos; full-page photo with a white title · 8–9 panorama across the spread with the title, three text columns · 10–11 title, text, big photo; drop cap text and photos · 12–13 three-column grid with a tall photo row, both pages · 14–15 drop cap text and stacked photos; inset photo with a white title · 16–17 full-bleed spread photo with a title · 18–19 title, text, tall photo; photos and three text columns · 20 back cover with the masthead, contacts and a photo

**Image slots:** one cool, slightly desaturated cover photo of a person in motion (`imagery.py grade` or Pillow colour 0.55); on-topic editorial photos, 5000 px for full pages and spreads (a spread needs 4200 px wide at 250 ppi); panorama and full-bleed spread photos use `.cross`

**Theme colours:** brand #111114; accent #2E5B8A.

**Deviations from the reference:** the reference shows 17 spreads built from these nine layouts; repeat archetype spreads to reach its page count

**Using it:** follow `reference/kit-flow.md` (`/folio:winter`). Fill every `data-kit-sample` element with the client's content (premium copy from thin input), make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings.
