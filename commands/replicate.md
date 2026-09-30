---
description: Copy reference pages 1:1 with your content; the style joins folio's catalogue only if it beats the closest existing style
argument-hint: "<reference image paths> [content]"
---
Use the folio skill to replicate these reference pages 1:1: $ARGUMENTS

1. **Read** `library/TASTE.md` (the user's bans still apply: no decorative horizontal rules; readable contrast). Gather the content facts into `source.md`.
2. **Study each reference:**
   - crop every page or slide and upscale it 2x;
   - measure page ratio, columns, colour blocks, image frames and type sizes as percentages of the page;
   - note the devices (title marks, hatches, bands, reflections, cut-outs, mockups) and the photo treatment.
   If a reference is too small to read, look for a larger preview of the same template online before guessing.
3. **Ask the rest with `reference/wizard.md`:**
   - round 1: logo, words;
   - round 2: colour from the logo, with the reference's own colours as option A; photos;
   - round 3: which references to build, contacts, pages. The page size defaults to the reference's own ratio for a true 1:1.
   Then the page plan for approval.
4. **Build it** with the reference's grid, proportions, colours and devices, the user's content (premium copy from thin input) and on-topic imagery (`imagery.py` grade, cutout, screenshot + mockup, logos, hatch, divide, reflect). Where the reference would fail print contrast or break a user ban, deviate minimally and say so. Show a first look (cover + first spread) before building the rest.
5. **Check:** render, compare every page side by side with its reference crop, preflight to 0 errors / 0 warnings, editable fidelity ≥ 97%.
6. **Deliver** with the still-to-fill list and record the verdict.
7. **Run the learn gate** (`reference/wizard.md` §9). The default is **not** to add the style: score it against the closest kit, and offer "Save as a new style?" only when it clearly beats it, breaks no ban and isn't a near-duplicate; otherwise say in one line why it wasn't added. On yes:
   - `python <skill>/scripts/kit.py save <project> <new-id> --name "…" --family "…" [--cmd <name>]`;
   - complete its `KIT.md` (looks, `best_for`, archetypes, image slots, theme colours, deviations);
   - `kit.py gallery`.
