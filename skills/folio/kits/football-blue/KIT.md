---
id: football-blue
name: Football Blue
family: sport & action
size: A4 (210 x 297 mm)
pages: 14
render: --bleed 3
fonts: Big Shoulders Display:800,900; Barlow Condensed:600,700,800,800i,900i; Familjen Grotesk:400,500,600,700
theme: brand #1D3FAA; accent #16307F
---
# Football Blue

**Looks like:** A royal-blue sports monthly: a cover with a ghost word, a huge white condensed masthead broken by a cut-out figure in full stride, a round hero object cropped at the edge, a year and cover lines, a barcode; white interiors with italic heavy titles, a contents list with arrows, a profile page on a blue panel with a giant number, a blue sidebar with a person placeholder, a band with diagonal white stripes and a cut-out line-up, a full-page advert, a quote with a cut-out, and a blue back cover. Dense like the reference (three-column text, stat rows, captions, fact boxes), navy panels for contrast, a faint diagonal texture on blue pages, and on every spread one element that runs across the fold: a navy note box (2–3), a navy stat band (4–5), a navy title band (6–7), the striped line-up band (8–9), an advert band (10–11), a cut-out reaching across (12–13). User reference 1:1.

**Page archetypes:** 1 cover · 2–3 contents with arrows and photos; welcome with a big photo and signature · 4–5 key projects with photo, circle photo and a stat row; photo top and a photo grid · 6–7 blue profile panel (cut-out, big word, giant number, white box); text columns, circle photo and photo · 8–9 blue sidebar with a person placeholder, text and photos; striped band with three cut-outs and three columns · 10–11 full-page advert (device mockup); photo top, side photo column and text · 12–13 photo, text, big quote with a cut-out; list with a blue photo sidebar · 14 blue back cover with ghost word, contacts and people placeholders

**Image slots:** one cut-out figure in motion for the cover (`imagery.py cutout --person`, 5000 px source), a round hero object cut out (the Earth, a ball, a product), three cut-outs for the line-up band, a device mockup of the client's own site for the advert (`imagery.py screenshot` + `mockup`), circle crops (`imagery.py reflect --shape circle --depth 0`), on-topic team and event photos

**Theme colours:** brand #1D3FAA; accent #16307F.

**Deviations from the reference:** the ball is the Earth; the car advert is an app-build advert; player profiles are service profiles (stock people are illustrations, never the client's team)

**Using it:** follow `reference/kit-flow.md` (`/folio:football`). Fill every `data-kit-sample` element with the client's content (premium copy from thin input), make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings.
