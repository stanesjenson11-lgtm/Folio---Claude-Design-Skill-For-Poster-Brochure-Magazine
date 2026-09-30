# extract — mine an existing PDF for a redesign

Use when the user supplies an old brochure/report to redesign (keep content, change the design) or a previous deliverable whose visual system must be reused (e.g. "make this year's report look like last year's quotation brochure").

```bash
python <skill>/scripts/harvest.py old.pdf --out harvest
```
Then:
1. **Look at `harvest/crops.png`.** Every visible crop, labelled. Flag crops that include captions, watermarks (phone GPS stamps), confetti/graphics or slivers of neighbouring photos. For each photo decide: re-crop from `native/` (preferred — it's the full original at native resolution) or keep the `visible/` crop. Write decisions to `harvest/crops.json` and re-run with `--overrides harvest/crops.json`, then look again. Never trust a crop you have not seen.
2. **Text.** `harvest/text/pNN.txt` gives the copy per page. Rebuild clean copy in a `copy.md` with headings marked; fix broken line-ends and hyphenation from extraction, but do not edit wording.
3. **Tokens.** `harvest/tokens.json` lists fill colours by area and fonts by use. Map them to roles (paper, ink, brand, tint, accent) and confirm with the user if the system is being reused. `pdffonts old.pdf` gives exact font names.
4. **Structure.** Render the old PDF to PNGs (`pdftoppm -r 60 -png old.pdf old/p`) and write a page list: what each page contains. This becomes the content column of the new FLATPLAN.
5. **Reusing a visual system** from a previous deliverable: extract its tokens and its recurring devices (header rail, callout boxes, footer pill…) into DIRECTION.md as named components, then build the new content with them — same system, new layouts where the content needs them.

**Redesign protocol** (after taste-skill). Decide once, with the user, whether this is **preserve** (same system, better craft) or **overhaul** (new system, same content). Change in this order and stop when the brief is met: typography → spacing and rhythm → colour → recomposition → full replacement. The logo, legal and regulatory copy, certification marks and approved figures never change without asking. Imported PDFs need hygiene first: merged words ("Weunderstand"), broken line ends, justified rivers.

Resolution check: `manifest.json` has `max_print_mm_at_250ppi` per image; use it when assigning photos to frames in the flatplan.
