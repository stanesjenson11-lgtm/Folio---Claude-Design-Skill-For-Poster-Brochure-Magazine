---
description: Pick one of folio's signed-off styles from the gallery and make a magazine or brochure from any content
argument-hint: "[content / website / brief]"
---
Use the folio skill to make a magazine or brochure from: $ARGUMENTS

1. Read `library/TASTE.md`, `kits/INDEX.md` and `kits/GALLERY.png` (tell the user the gallery's path so they can open it). Gather the facts first (their content, website, card) into `source.md`.
2. Ask once with the question tool (max 4 questions):
   - **Family:** Sport & action · Editorial & minimal · Pop & colour · Business & news (list the kits in each family from `kits/INDEX.md` in the question text).
   - **Style:** the kits in the chosen family (name + one-line look; recommend the best fit for the content).
   - **Theme colour:** the kit's own colours · my brand colour (ask for the hex or read the logo with `palette.py --from-image`) · you choose.
   - **Pages:** 8 · 12 · 16 (default to the kit's own count).
3. Then follow `reference/kit-flow.md` from step 3 with the chosen kit. In short: `python <skill>/scripts/kit.py new <kit> <project> [--brand #hex --accent #hex] --name <file>`, then follow the kit's `KIT.md`: fill every `data-kit-sample` element with premium copy from the facts (`reference/copy.md`, anything inferred gets `data-sample`), make each photo slot with its recipe from the client's own world, keep the kit's page roles and continuity devices, add or drop archetype pages to reach the page count.
4. Render (`render.py <file>.html` + the kit's render flags), look at every page, preflight to 0 errors / 0 warnings, editable fidelity ≥ 97%.
5. Deliver the PDF + editable HTML, ask which pages work, and record the verdict (`reference/taste.md`).
