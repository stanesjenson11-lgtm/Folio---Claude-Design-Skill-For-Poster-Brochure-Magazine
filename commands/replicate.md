---
description: Copy reference pages 1:1 with your content, then save the style to folio's catalogue
argument-hint: "<reference image paths> [content]"
---
Use the folio skill to replicate these reference pages 1:1: $ARGUMENTS

1. Read `library/TASTE.md` (the user's bans still apply: no decorative horizontal rules; readable contrast). Gather the content facts into `source.md`.
2. Study each reference: crop every page or slide and upscale it 2x; measure page ratio, columns, colour blocks, image frames and type sizes as percentages of the page; note the devices (title marks, hatches, bands, reflections, cut-outs, mockups) and the photo treatment. If a reference is too small to read, look for a larger preview of the same template online before guessing.
3. Ask once (question tool): which references to build, page count, page size (the reference's own ratio is the default for a true 1:1).
4. Build it with the reference's grid, proportions, colours and devices, the user's content (premium copy from thin input) and on-topic imagery (`imagery.py` grade, cutout, screenshot + mockup, logos, hatch, divide, reflect). Where the reference would fail print contrast or break a user ban, deviate minimally and say so.
5. Render, compare every page side by side with its reference crop, preflight to 0 errors / 0 warnings, editable fidelity ≥ 97%.
6. Deliver, record the verdict, and when the user likes it save the style: `python <skill>/scripts/kit.py save <project> <new-id> --name "…" --family "…" [--cmd <name>]` (this also creates its `/folio:<name>` command), complete its `KIT.md` (looks, archetypes, image slots, theme colours, deviations) and rebuild the gallery (`kit.py gallery`).
