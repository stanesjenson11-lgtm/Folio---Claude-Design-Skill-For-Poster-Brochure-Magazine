---
id: newsletter
name: Business Newsletter
family: business & news
best_for: company newsletters, internal news, NGOs, schools, updates; newsy and trustworthy; black-and-white team and office photos, portraits; 8 pages
size: A4 (210 x 297 mm)
pages: 8
render: --bleed 3
fonts: Young Serif:400; Familjen Grotesk:400,500,600,700
theme: brand #2C8535
---
# Business Newsletter

**Looks like:** A newspaper-style company newsletter on light paper: a serif masthead (name + weekly line, a green edition box, a huge NEWSLETTER word, a date line with vertical separators), two news teasers with square photos, a big black-and-white photo with a green headline box overlapping it; inside, green header tabs (one crossing the fold), black-and-white team photos with green blocks overlapping them, serif headlines, green quote boxes with circle portraits, black text boxes, an outlined quote box, a full green page, and a "Thank You" back cover. User reference 1:1.

**Page archetypes:** 1 cover · 2–3 team photo + overlapping green block + small photo column; photo over a green panel, headline, quote, circle portrait over a black box · 4–5 photo + uppercase headline + byline + body, subhead + circle portrait with name; big photo, headline + body, green quote box with circle portrait · 6–7 big headline, text column, tower photo, outlined quote box; full green page with headline, text, photo and a two-column black box · 8 back: team photo + green "Thank You" box with contacts and credits

**Image slots:** black-and-white photos (`imagery.py grade --treatment bw`): the client's team or on-topic teams at work, one upward architecture shot for the cover, one for the feature; circle portrait placeholders for named people until photos arrive

**Theme colours:** brand #2C8535 (swap with `--brand`; keep it dark enough for small white text, 4.5:1).

**Deviations from the reference:** no horizontal rules (user ban, masthead rules included); green deepened from #42A24B so small white text passes print contrast; serif heads in Fromage → Young Serif

**Using it:** follow `reference/kit-flow.md` (`/folio:newsletter`). Fill every `data-kit-sample` element with the client's content, make each photo slot with the recipe above, keep the page roles, then `render.py <file>.html --bleed 3` and preflight to 0 errors / 0 warnings.
