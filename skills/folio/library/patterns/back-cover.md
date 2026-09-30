---
id: back-cover
family: closer
registers: [corporate, catalog, magazine]
loud: false
seen_in: ["ref-01 back cover arc + tagline", "ref-04 back cover QR", "ref-08 'THE END' back"]
---
# Back cover

**Why it works:** The back cover closes the motif: the same arc/slab/colour as the front, a second photo or plain field, a one-line sign-off, logo and contacts. It should look like the front's quieter sibling.

**Anatomy**
```
┌─────────────────────┐
│ ░░PHOTO░░(arc)▓▓▓▓▓ │   motif from the cover, mirrored
│ ▓▓▓▓ Learning with  │   short sign-off (tagline) large
│ ▓▓▓▓ Kindness…      │
│ tagline line  logo  │   contacts, URL, QR (tested!)
└─────────────────────┘
```

**Rules**
- Repeat the front's motif mirrored or rotated, and give the page a composition: an image or layered element, a large sign-off, then the contacts. Never a plain list of contacts on a flat ground (user verdict).
- Contacts complete and checked: phone, email, address, website.
- QR codes: ≥ 20mm, quiet zone, tested with a phone before printing.

**Goes generic when**
- A copy of the front cover.
- Contacts in 6pt grey.

**Build notes:** Reuse the cover classes with a `.back` modifier; generate QR via the `qrcode` Python package as SVG.
