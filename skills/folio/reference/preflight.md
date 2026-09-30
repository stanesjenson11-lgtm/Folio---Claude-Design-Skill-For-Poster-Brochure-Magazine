# preflight — before anything leaves

```bash
python <skill>/scripts/render.py brochure.html --bleed 3            # print version
python <skill>/scripts/preflight.py brochure.html --pdf out/brochure.pdf [--target digital] [--brand-fonts "Poppins"]
```
Exit code 1 means ERRORs remain; do not deliver. The report prints a rhythm strip (■ loud / □ quiet) — compare it with FLATPLAN.md.

Add `--copy copy.md` whenever the client supplied copy: every source sentence must appear verbatim in the layout (catches paragraphs dropped during copyfitting).

## What it measures
- ERROR: hidden overflow (text clipped by a box or the page), text off the trim, missing images, type < 6.5pt, placeholder/TK copy, effective image resolution below the floor, fallback or non-embedded fonts in the PDF.
- WARN: text in the safe zone or near the spine, text-on-text collisions, measures > 82 characters, contrast below WCAG, images below target ppi, masked shapes cut by the spine, and the web-UI tells (box shadows, side stripes, rounded card grids, gradient text, emoji headings, reflex fonts), plus layout monotony across pages.
- WARN (page fill): quiet text pages whose content stops far above the bottom margin (ragged foot) or that have an empty band mid-page — mark real openers/hero pages with `data-type="opener|hero|closing"` or `data-intent="breathing"`.
- ERROR (copy): client sentences missing from the layout (`--copy`).
- INFO: text over photos (verify in the PNG), underfilled pages, missing folios, all-quiet rhythm, generic marketing / AI words, dash-heavy prose.
- WARN (copy tells, from humanizer): not-X-but-Y contrasts and slogan rows of fragments. Hits that come from the client's own copy (`--copy`) are skipped. See `reference/copy.md`.

`rotated-heading` (WARN): text of 30pt or more set vertically or rotated. Poster variants: `variant-clash` (WARN) when two `data-variant` pages share a heading font, heading position, heading colour or ground colour. `.single` pages skip the spine checks; `data-variant` pages skip `dup-image` (a speaker can repeat). `--source client.md` keeps AI-tell scanning on folio's own rewritten `--copy`.

Mark intentional exceptions in the HTML rather than ignoring output: `data-allow-round` (rounded pills and cards that are the style's motif), `data-allow-edge`, `data-allow-overlap`, `data-intent="breathing"`, `data-no-folio`. Client brand fonts that happen to be on the reflex list go in `--brand-fonts`.

## What only eyes can check (do it on the PNGs)
Legibility of text over photos; crops; colour harmony; that page order and folios match the flatplan; names, titles, phone numbers and figures against the source copy; logo clear space; that the cover works as a thumbnail (look at it at 15% size).

## Printer handoff notes (tell the user)
Print PDF has 3mm bleed; ask the printer whether they want crop marks and CMYK conversion themselves (most digital printers accept RGB PDFs; offset printers may request PDF/X — they can convert, or use Ghostscript/Acrobat). Always ask for a hard proof for brand colours.
