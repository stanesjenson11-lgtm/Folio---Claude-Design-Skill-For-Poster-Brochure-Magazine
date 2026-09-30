---
id: estimate-sheet
family: data
registers: [catalog]
loud: false
seen_in: ["house-10 turf quotation: estimate, bank details, terms, sign-off"]
---
# Estimate sheet

**Why it works:** The price page is where the client decides. Everything they need to act on (what, how much, tax, validity, how to pay, who signed) sits on one page in the order they ask.

**Anatomy**
```
┌──────────────────────────────────────┐
│ Ref · Date · Valid until             │
│ #  Item         Qty  Unit  Rate  Amt │  hairlines + zebra tint only
│ 1  Turf supply  …    sqft  …     …   │
│ 2  …                                 │
│                  Subtotal     ₹ …    │
│                  GST 18%      ₹ …    │
│                  TOTAL        ₹ …    │  total + amount in words
│ Rupees Fourteen Lakh Fifty Thousand  │
│ Bank details   │  For, COMPANY       │  signature, name, role, stamp
│ Terms: numbered, 2 columns, tax and validity first │
└──────────────────────────────────────┘
```

**Rules**
- Currency symbol, quantity, unit and rate on every line; Indian grouping (14,50,000) for INR.
- Tax, validity and payment terms visible, not buried at clause 10.
- Terms as numbered clauses in two columns; warranty as its own short table.
- Every figure comes from the client's approved estimate; folio never computes, rounds or fills in a price without asking.

**Goes generic when**
- A fully boxed table with every border drawn.
- A single lump sum with no scope lines.

**Build notes:** `data-tint` table styles; `font-variant-numeric: tabular-nums`; the amount in words is supplied or checked against the figure by the client.
