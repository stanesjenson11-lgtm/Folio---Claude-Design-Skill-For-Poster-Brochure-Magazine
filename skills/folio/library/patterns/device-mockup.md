---
id: device-mockup
family: image
registers: [catalog, corporate, magazine]
loud: false
seen_in: ["user reference 2026-09-29: 'Portfolios' phone, tablet and desktop mockups"]
---
# Device mockup

**Why it works:** For a tech or digital client, its own screens on a phone, tablet or desktop are the most honest proof of the work, and far more specific than stock.

**Rules**
- Capture the client's real site or app: `imagery.py screenshot <url> --device desktop|tablet|phone --out shot.png`.
- Frame it: `imagery.py mockup --device desktop|tablet|phone --screen shot.png --out m.png` (flat bezel, no shadow).
- One device per page at hero size; the device stands on or overlaps a colour field edge.
- Only show screens the client owns or built, never someone else's product as theirs.
