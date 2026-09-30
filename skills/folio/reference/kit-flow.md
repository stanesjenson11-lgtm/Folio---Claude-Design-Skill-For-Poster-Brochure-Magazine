# kit flow — make a piece from a catalogue style

Used by every style command (`/folio:magazine`, `/folio:night`, `/folio:popart`, `/folio:portfolio`, `/folio:profile`, `/folio:ebook`, `/folio:sports`, …) and by `/folio:styles` once a kit is chosen.

1. **Read** `library/TASTE.md` and the kit's `kits/<id>/KIT.md`; look at `kits/<id>/preview.jpg`. Gather the client's facts (their content, website, card) into `source.md`. Never invent facts; anything inferred gets `data-sample`.
2. **Ask once** (question tool, ≤ 4 questions): theme colour (the kit's own, recommended · my brand colour, hex or logo via `palette.py --from-image` · you choose); pages (the kit's own count, recommended · fewer · more, by dropping or repeating archetype pages); anything the content can't answer (e.g. which imagery world when the subject isn't obvious). Skip questions the user already answered.
3. **Start it:** `python <skill>/scripts/kit.py new <id> <project> [--brand #hex --accent #hex] --name <file>`.
4. **Fill it:** replace every element marked `data-kit-sample` (preflight ERRORs until you do) — premium copy from the facts (`reference/copy.md`), each photo slot made with the kit's recipe from the client's own world (`/folio:stock` for photos, `imagery.py` for grades, cut-outs, screenshots + mockups, logos, sketches). Keep the kit's page roles, devices and continuity; after a colour swap use `var(--on-brand)` / `var(--on-accent)` for text on colour fields.
5. **Check it:** render with the kit's flags (`render.py <file>.html …`), look at every page, preflight to 0 errors / 0 warnings, editable fidelity ≥ 97%.
6. **Deliver** the PDF / PNGs + editable HTML, ask which pages work, record the verdict (`reference/taste.md`).
