# craft — build the book end to end

## 0. Intake
No DIRECTION.md? Run the intake gate first (`reference/intake.md`) — pre-flight scan, Design Read, swatches, one round of questions, lock. Then `brief` for the flatplan.

## 0b. Preconditions
BRIEF.md, FLATPLAN.md and DIRECTION.md exist (run `brief` / `direction` first; for a small job — a flyer, a 4-page leaflet — you may fold them into a short plan in chat). Fonts fetched:
```bash
python <skill>/scripts/fonts.py "Archivo:400,600,800" "Source Serif 4:400,400i,600" --out fonts
# Tamil or other scripts: add --subsets latin,latin-ext,tamil and a font that covers it (Hind Madurai, Mukta Malar, Noto Sans Tamil)
```

## 0c. Photos
Copy originals to `img/raw/`, then unify them: `python <skill>/scripts/imagery.py grade img/raw --out img --match` (or the direction's treatment). Generate the direction's motif if openers need it (`imagery.py motif`).

## 1. Skeleton
Copy `assets/starter.html` to `brochure.html`, copy `assets/folio.css` next to it (so the project is self-contained), and write `tokens.css`. One `<section class="page">` per flatplan row, in order, each with a comment naming page number, side and pattern:
```html
<!-- 04 · V · spread 4–5 · photo-crossing-gutter -->
```

## 2. Build pattern by pattern
Open each pattern card the flatplan uses and follow its anatomy. Placement tools, all in mm/pt:
- text blocks: children of `.live`, placed with `grid-column` / `grid-row` on the 12×16 grid;
- photos and colour fields: `.ph` / `.box` inside `.trim`, positioned with `inset`, using `var(--b0)` on every edge that touches the trim so it bleeds;
- a photo across the gutter: the same `.spread-img` on both pages of the spread;
- masks: `.mask-circle`, `.mask-arc-l/-r`, `.mask-slant`, or a project clip-path from the motif;
- furniture: `<footer class="furniture"><span class="run">Section</span><span class="folio-num">07</span></footer>`;
- intentional exceptions for preflight: `data-allow-edge` (type bleeding off the page), `data-allow-overlap` (type over type), `data-intent="breathing"` (deliberately empty page), `data-no-folio`.

Author for the editable export: every visible thing is a real element (no `::before`/`::after` stripes or labels), text lives in `p`/`h*`/`span`/`div` elements, charts are inline SVG, and colour fields are elements with a background colour. `render.py` warns about anything it cannot export.

Write page-specific CSS in a `<style>` block or `pages.css`, scoped by a class on the page (`.p-cover`, `.p-director`). Keep every size in pt/mm.

## 3. The look loop (non-negotiable)
After every 2–4 pages:
```bash
python <skill>/scripts/render.py brochure.html --pages 1-4      # PDF + PNGs + contact.png
```
Open `out/contact.png` and each new `out/pages/p-XXX.png` with the image viewer and look like an art director: Is there one dominant element per spread? Does the eye land where it should? Are edges aligned across the spread? Is anything cramped against a margin? Are crops cutting heads or hands? Does text on photos read? Fix, re-render, look again. Code that "should" work is not evidence; the PNG is.

## 4. Copyfit
Text that doesn't fit is fixed in this order: adjust the layout (column span, image size, page pattern) → add a page (respecting binding multiples) → tighten leading/tracking within the register's ranges → ask the client to cut. Never drop below the register's body size and never cut client copy silently.

## 5. Finish
Run the six-axis self-critique (critique.md) and write the stamp. Run `polish`, then `preflight` (with `--copy copy.md`) until it reports zero errors and every warning is either fixed or consciously accepted, then `export`. Check the editable fidelity numbers in render.py's output (≥ 97% per page). If you found a defect that would recur on another job, apply the self-improvement loop in SKILL.md. Offer `promo` once the user is happy. Summarise: direction in one line, page count, what's still TK, what the user should check in the proof (colours on paper, names spelled right).
