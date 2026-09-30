---
id: pop-stripe
name: Pop Stripe (Pop Art)
family: pop & colour
size: 16:9 (320 x 180 mm)
pages: 10
render: --single
fonts: Familjen Grotesk:400,600,700; Bodoni Moda:400,500
theme: brand #FFC20E; brand-2 #FFD84A; brand-3 #FFD54A; accent #C2410C; accent-2 #F58A07; accent-3 #F7A21B
---
# Pop Stripe (Pop Art)

**Looks like:** Bright landscape pages in vertical stripes of light grey, white and the brand colour; photos in circles and rounded squares that cross the stripe edges with a faded mirror reflection; pairs of small gradient cards; a serif two-line head with a small eyebrow and a spaced-caps label; icon bullets in colour discs; the logo in a corner and three dots as a pager. Friendly, glossy, pop. User-loved (1:1 replica of their 'Pop Art' reference).

**Page archetypes:** 1 cover (grey + white stripe, brand block, two-tone word across the split, circle photo) · 2 about (two circles over the brand block) · 3 what we build (brand block, rounded photo with reflection, white stripe with logo) · 4 how we work (white panel, brand column with two rounded photos, three icon bullets) · 5 delivery (brand panel note, full-height photo, white panel) · 6 feature (big disc + circle photo) · 7 feature (rounded white card, two rounded photos) · 8 two-column feature (brand block top-left, two rounded photos) · 9 proof (photo quadrants) · 10 contact (full-height photo, brand stripe)

**Image slots:** photos toned to the brand (`imagery.py grade --treatment duotone --brand <brand>`); circle and rounded crops with reflections (`imagery.py reflect <photo> --shape circle|rounded --size WxH`); the client's logo in ink and white (alpha silhouettes)

**Theme colours:** brand #FFC20E; brand-2 #FFD84A; brand-3 #FFD54A; accent #C2410C; accent-2 #F58A07; accent-3 #F7A21B (swapped by `kit.py new --brand/--accent`; variants keep their lightness offset).

**Deviations from the reference:** the cover's second word is a deep accent instead of white on yellow; eyebrows on white are deep accent; both for print contrast

**Using it:** `kit.py new pop-stripe <project> [--brand #hex --accent #hex] --name <file>` → fill every `data-kit-sample` element with the client's content (premium copy from thin input, `reference/copy.md`), make each photo slot with the recipe below, keep the page roles, then `render.py <file>.html --single` and preflight to 0 errors / 0 warnings. After a colour swap, set any text that sits on a brand or accent field to `var(--on-brand)` / `var(--on-accent)` if preflight reports contrast. Drop or duplicate archetype pages to reach the page count; keep the rhythm (loud / quiet) and the continuity devices.
