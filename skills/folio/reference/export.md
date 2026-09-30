# export — deliverables

| Deliverable | Command | Notes |
|---|---|---|
| Print PDF | `render.py brochure.html --bleed 3` | trim + 3mm bleed per side; tell the printer the trim size |
| Screen PDF | `render.py brochure.html` | trim size, no bleed; for email/WhatsApp/web |
| Page PNGs + contact sheet | produced by every render | `out/pages/`, `out/contact.png` — use for client previews and social posts |
| **Editable page-embedded HTML** (default, every render) | `render.py brochure.html` (or `editable.py brochure.html`) | flat HTML: one absolutely positioned element per text block, shape and image; images cropped at native resolution with masks baked in; fonts via Google Fonts link + embedded base64; pages `data-document-role="page"` at trim size (A4 = 794 × 1123 px). A fidelity check compares each page with the original (≥ 97% expected) and writes `out/editable-diff.png` when a page falls short |
| Posters / single pages | `render.py poster.html --single` | contact sheet without spreads |

`--no-editable` skips it; the old `--canva` flag is accepted but no longer needed.

For Canva: the Canva connector's `import-design-from-url` needs a public URL; otherwise the user uploads the `.canva.html` / PDF in Canva. Keep the layout as positioned elements rather than deeply nested flex/grid if the user plans heavy editing in Canva — imports flatten more predictably. Check the imported result page by page; editable text and separate image layers are the goal.

Screen PDFs can be large with full-resolution photos; if the user needs a small file for WhatsApp/email, downscale images to ~150 ppi at their printed size before a screen render (keep originals for print).

Before any export: `preflight.py` with zero errors.
