# formats: single sheets, folds and large format

Folio's print rules assume a bound book. Posters, flyers, folded leaflets and large-format panels keep the same principles (one dominant element, scale contrast, real photos, no template chrome) but read differently. Read this for any piece that is not a bound multi-page document.

## Sizes
`<html data-size="…">` in folio.css: `A4`, `A4-landscape`, `A5`, `A3`, `A2`, `Letter`, `Letter-landscape`, `DL`, `square-210`, `magazine`. Anything else: `<html data-size="custom" style="--pw:600mm;--ph:900mm">`. Render with `render.py --single` for a contact sheet of single pages.

## Poster variants (the default for any poster request)
Make **4 designs, each unique on every axis**, not one design in four colours, and build them **inside the user's preferred family** from `library/TASTE.md` (currently `arc-stage`): the family sets the grammar, the variants vary it. Build them from 4 layout archetypes × 4 token sets, one each:

| Axis | Must differ between every pair of variants |
|---|---|
| Heading font | a different family per variant (pairs in `typography.md` → Poster pairs) |
| Header position | e.g. crossing the photo's foot · across the photo's top edge · under the photo · left, crossing its side edge. Always horizontal |
| Colours | ground, heading colour, body colour and accent |
| Texture | concentric arcs · rings centred on the photo · arcs from a corner · soft blobs behind the photo (`imagery.py motif`); liquid and pencil only on request |
| Photo | plain rectangle, portrait or square: vary its size and position (centred, offset right, tall, crossing the top), not its outline |
| Info block | rounded card bottom-right · rounded card bottom-left · pill chips · stacked column |

**Layered ground (every poster):** never a flat colour. Stack, from the back: the ground colour or glow gradient → `imagery.py motif --type glow` (soft white blooms, vector) → the family texture (arcs, rings, blobs) at 35–55% → `motif --type dots` (fine dots, densest near one corner) → `imagery.py texture --kind paper|grain` at 20–40% opacity. Keep the photo and all text above these layers, and keep the layers quiet behind text.

Mark each page `<section class="page single" data-variant="<name>" data-allow-round>`; preflight's `variant-clash` check compares heading font, heading position, heading colour and ground colour between every pair and warns on any repeat. A weekly **series** with the same rails every week (`series-rail`) is only for when the user asks for consistency.

**Deliver** PNG + Canva-editable HTML, no PDF: `render.py poster.html --png-only --dpi 300` (A3/A2 print) or `--dpi 96` (1080 px social). Textures stay editable in Canva because they are vector SVG; never put a clip-path on a colour-field `div` (Canva flattens it to a rectangle — editable.py warns). Finish every set by asking which variants work and recording the verdict (`reference/taste.md`).

Worked example: `thursday-service/` next to the plugin (`make.py` builds four variants from `weeks.json`).

## Poster (A3, A2, social)
- **Three reads, in order:** what it is (the event or offer, top third, the biggest thing on the sheet), who or what (face, product or building), when/where/how (one block). Everything else is small.
- **One info block.** Date, time, venue and CTA sit together in one module opposite the figure, in one date format across the series ("Thursday 9 October 2025 · 6:30 pm"). Never scatter them.
- **QR codes** get a label that says what they open ("Scan for directions"), sit in the info block or the foot, never mid-sheet, and are at least 20mm on A3.
- **Viewing distance.** A3 on a notice board is read from 1–2m: the event name at least 8% of sheet height, body no smaller than 11pt, footer credits no smaller than 9pt.
- Patterns: `speaker-poster`, `numeral-window`, `bilingual-lockup`; `full-bleed-opener` with the headline in the photo's quiet area.

## Poster series (weekly services, event programmes, social sets)
Consistency lives in fixed rails; the body varies. See `series-rail`. Lock the rails, the date format, the type pair and 2–3 colour lanes before the first poster; the series then changes photos and words only. Check a new poster by placing it next to the last three: it should read as the same series from across the room.

## One-page flyer (A4, A5, Letter)
Photo band 40–50% of the height (the client's real place or product) → one concrete headline → 2–4 proof points with numbers, certifications or client names → a foot strip with logo, contact and QR. The logo and contact details are mandatory; a flyer without them is a defect. Brand colour is required. No "Why choose us?" icon card.

## Trifold (A4 or Letter landscape, roll fold)
Imposition follows the fold, not the reading order:
```
OUTSIDE   [ tuck flap | back cover | front cover ]
INSIDE    [ inside 1  | inside 2   | inside 3    ]
```
- The **middle outside panel is always the back cover:** contact, address, QR, map.
- The **tuck flap** (outside left, which folds in) is 1.5–3mm narrower than the other panels. On A4 (297mm): 97 · 100 · 100; on Letter (279.4mm): 91.4 · 94 · 94. Never equal thirds.
- **First opening** shows inside 1 beside the tuck flap: pair them (introduction + first proof). The full inside spread tells the product or offer story.
- **Cover** = logo, one headline, one image. Service lists go inside.
- Keep type at least 6mm from folds; nothing important crosses a fold.
- Alternate panel grounds (dark/light) so every folded state has contrast.
- Design both sides. A single-sided multi-column sheet is a poster, not a trifold.
- Build: two `.page` elements (outside, inside), each a 3-column grid with the panel widths above (outside `97mm 100mm 100mm`; inside `100mm 100mm 97mm`, because the tuck flap's reverse is inside 3). Draw fold guides only while checking the layout; delete them before the final render.
- Z-fold: panels are equal and read left to right on both sides; the outside right panel is the cover.

## Large format (stage backdrops, trade-show walls, banners)
- **Read from 2–5m.** The name or event reads at the back of the room: cap height at least 4% of panel height. At most 6 lines of body per panel.
- **Stage backdrop:** people stand in front of it. Marks (logo, wordmark, anniversary badge) live in the top 20% on one baseline; the middle stays quiet (a ghost emblem at 25–40% contrast at most); the lower half is texture, because heads and the podium cover it.
- **Trade-show walls:** one job and one hero per panel (brand + product / proof / certifications / contact). Brand lockups in fixed corners across the set. Nothing important below knee height (~50cm) or above 2.2m.
- **Resolution at size:** photos at 100–150 ppi at final size are enough for viewing from 2m+. Check `max_print_mm_at_250ppi` and scale the threshold, or ask for originals.
- **Very large pages:** PDF pages top out at 200 inches (5080mm). Design at 1:10 (`--pw:731.5mm` for a 24ft wall) and tell the printer the scale, or ask for their template.
- Ask the printer for bleed and safe zones: flex and fabric prints often want 25–50mm, not 3mm.
