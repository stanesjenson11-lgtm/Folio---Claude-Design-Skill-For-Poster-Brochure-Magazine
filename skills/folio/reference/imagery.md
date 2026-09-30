# imagery — visuals from the project's own context

Photographs of the real organisation always come first. `scripts/imagery.py` fills the gaps and unifies what exists.

## grade — make mixed photos look like one shoot
Client photos arrive from five phones under different light. Before layout:
```bash
python <skill>/scripts/imagery.py grade img/raw --out img --match                          # natural, unified
python <skill>/scripts/imagery.py grade img/raw --out img/duo --treatment duotone --brand "#1f3fb0" --ink "#10131f"
```
Treatments: `natural` (levels + gentle white balance), `duotone` (ink → brand → paper — rescues weak or low-quality photos and makes them a design element), `bw`, `tint`. Choose one treatment per book in DIRECTION.md; mixing treatments on a spread looks accidental. Keep originals; never grade over them.

## Sketches — the default image style for brochures (user taste)
```bash
python <skill>/scripts/imagery.py sketch img/raw/photo.jpg --out img/photo-sketch.png --palette "#3B2A20,#7D8B6A,#C9A96E,#F6F1E7" --max 1800
```
Coloured-pencil drawing on transparent paper: the darkest palette colour draws the lines, the middle colours lay the strokes, the lightest is the paper. Soft irregular edge, no rectangle. See `library/patterns/sketch-spot.md`. People cut-outs: `imagery.py cutout photo.jpg --person` (rembg[cpu]).

## Flow shapes — curves that stay editable in Canva
```bash
python <skill>/scripts/imagery.py motif --type liquid --colors "#1d6f86,#3A1638,#F4B04A" --level 0.78 --amp 0.03 --bg none --w 303 --h 426 --out img/waves.svg
python <skill>/scripts/imagery.py motif --type blob --colors "#E9B872,#C8642E" --bg none --w 230 --h 270 --out img/blobs.svg
python <skill>/scripts/imagery.py motif --type pencil --accent "#0E2A47" --lines 15 --stroke 0.75 --bg none --w 303 --h 210 --out img/water.svg
python <skill>/scripts/imagery.py mask --shape wave-top|wave-bottom|blob --seed 3 --amp 6     # prints clip-path: polygon(…)
```
`liquid` = layered wave bands (use `--level` so text on the front band never meets a wave crest); `blob` = organic fields kept inside their canvas (show with `object-fit: contain`); `pencil` = hand-drawn water lines (tapered, jittered double strokes with pencil lifts). All are seeded, vector, and use presentation attributes only (no filters, no CSS classes), so the editable export keeps them. Paste the `mask` output as the `style` of a `.ph` frame — only when the user asks for curved photo frames (their recorded taste is plain rectangles).

## motif — vector backgrounds from the context
```bash
python <skill>/scripts/imagery.py motif --context "football turf academy" --brand "#0e1210" --accent "#b6f23a" --out img/motif-cover.svg
```
Types: `arcs` (institutions), `rings` (finance), `halftone` (magazines, sports), `slabs` (industrial), `grid` (tech, research), `pitch` (football/turf), `track` (athletics), `contour` (land, farms, real estate). Without `--type`, the context picks one. Output is vector SVG at trim size — use it as a `.fill` layer on openers, dividers and back covers, or behind stats. It is texture: keep it at low contrast behind text, and use at most one motif family per book (it should be the direction's motif).

## prompt — image-generation prompts
```bash
python <skill>/scripts/imagery.py prompt --context "organic vegetable farm at dawn" --role opener --palette "#7cb518,#2d5a27"
```
Roles: `hero`, `opener`, `texture`, `spot`, `background`. The prompt combines lighting, lens and a composition anchor that leaves room for type, plus a fixed avoid-list (text, logos, gradients, distorted hands). Run it through a connected image generator — the Canva connector's `generate-image`, the Adobe connector (Firefly) — or any model the user has.

Rules for generated images:
- Only for textures, backgrounds, objects and generic settings. Never people, buildings, products, events or results presented as the client's own — that misrepresents the organisation.
- Tell the user which images are generated; add "Illustrative image" in the credits when the client's policy requires it.
- Check the pixel size: many generators return 1–2 megapixels — fine for a small frame, not a full A4 page (needs ~2480 × 3508 px).

## cutout — magazine cut-outs
`python <skill>/scripts/imagery.py cutout img/player.jpg --out img/player-cut.png` (needs `pip install rembg`), or the Canva/Adobe background-removal tools. Inspect hair and fingers at 200% before placing with `.ph.cutout`.

## Stock photos
Only when the user agrees and the licence allows print use (the Adobe connector exposes Adobe Stock). Search for the physical subject ("turf floodlights at dusk, empty pitch"), not the category ("sports").

## Screens, devices, logos and pop shapes (v0.7)
- `imagery.py screenshot <url> --device desktop|tablet|phone [--scroll px]`: the client's own site, captured at 2x; `imagery.py mockup --device … --screen shot.png`: a flat device frame (no shadow). Use for any digital client.
- `imagery.py logos react,nextdotjs,…`: single-colour technology logos (Simple Icons). Only tools the client really uses, in one ink colour; credit "trademarks of their owners".
- `imagery.py hatch --shape circle|rounded|bracket|half|triangle|chevrons`: the hatched accents of the split-pop style.
- `imagery.py divide --edge top|bottom|both`: colour fields with a flowing edge for areas that cross a spread (`flow-divide`).
- `imagery.py reflect photo.jpg --shape circle|rounded --size WxH`: pop-stripe crops with a faded mirror reflection baked in (Canva keeps it).
- Rotations: bake them into the file; the editable export does not reproduce CSS-rotated images.
