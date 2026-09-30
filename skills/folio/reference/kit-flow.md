# kit flow: make a piece from a catalogue style

Used by every style command (`/folio:ivory`, `/folio:night`, `/folio:popart`, `/folio:portfolio`, `/folio:profile`, `/folio:ebook`, `/folio:sports`, `/folio:football`, `/folio:skate`, `/folio:winter`, `/folio:newsletter`, and the user's own `/folio-<name>` styles), where the style is already chosen. `reference/wizard.md` also uses it from step 3, once a kit has been picked.

1. **Read** `library/TASTE.md` and the kit's `KIT.md` (`kit.py list` finds shipped and user kits). Look at its `preview.jpg`.
2. **Ask the rest with the wizard** (`reference/wizard.md`), with **Style = this kit** already answered:
   - scan everything supplied;
   - round 1: logo, words (What is the kit's family);
   - round 2: colour from the logo, saying for each palette whether it suits this kit (the kit's own colours are always an option); photos. Skip Kind;
   - round 3: contacts, pages. Skip Style;
   - then the page plan for approval.
   Skip any question the user already answered.
3. **Start it:** `python <skill>/scripts/kit.py new <id> <project> [--brand #hex --accent #hex] --name <file>`.
4. **Fill it:** replace every element marked `data-kit-sample`; preflight ERRORs until you do.
   - Copy: premium, from the facts (`reference/copy.md`).
   - Photos: make each slot with the kit's recipe, from the client's own world (`/folio:stock` for photos; `imagery.py` for grades, cut-outs, screenshots + mockups, logos, sketches), placed as the approved plan says.
   - Keep the kit's page roles, devices and continuity.
   - After a colour swap, use `var(--on-brand)` / `var(--on-accent)` for text on colour fields.
5. **Check it:**
   - show a first look (cover + first spread, wizard §8) before building the rest;
   - render with the kit's flags (`render.py <file>.html …`) and look at every page;
   - preflight to 0 errors / 0 warnings; editable fidelity ≥ 97%.
6. **Deliver** the PDF / PNGs + the editable HTML with the still-to-fill list. Ask which pages work, record the verdict (`reference/taste.md`), and offer to save the client's brand (wizard §8).
