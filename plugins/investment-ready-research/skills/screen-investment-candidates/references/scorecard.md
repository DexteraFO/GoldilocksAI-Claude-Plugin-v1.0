# Mandate fit scorecard

Hard gates are checked before scoring. The score measures fit to the stated mandate, not the probability of returns or investment quality in isolation.

| Dimension | Max points | What earns points |
|---|---:|---|
| Sector/product fit | 20 | Direct match to target category and business model. |
| Revenue/size fit | 20 | Current or recent sourced figure aligns with band; a dated range can receive partial points. |
| Geography | 10 | Headquarters, primary market, or operations match the stated criterion. |
| Thesis mechanism | 20 | Specific, sourced product, customer, channel, or unit-economics evidence supports the thesis. |
| Commercial momentum | 15 | Dated growth, expansion, retention, customer adoption, or other mandate-relevant signals. |
| Transaction feasibility | 15 | Ownership, cap table/transaction context, or public status supports the requested deal type. |
| **Total** | **100** | |

Assign 0–max points per dimension with a one-sentence rationale and source IDs. Do not treat absence of evidence as evidence of zero performance. For a dimension with insufficient evidence, mark `Unknown` and retain its max points as uncertainty. Report:

- `Supported points`: sum of points awarded in assessed dimensions.
- `Possible score`: supported points through supported points plus max points of unknown dimensions; e.g. `62–82/100 (provisional)`.
- `Evidence coverage`: assessed maximum points divided by 100; e.g. `80%`. This is coverage, not a statistical confidence interval.

If all dimensions are assessed, show the computed integer `/100` and the coverage. If a dimension has only partial evidence, give a conservative assessed score with an explicit caveat or mark it Unknown; never use false decimals. Rank eligible names by supported points, then coverage, while visibly flagging overlapping score intervals. If coverage is below 70%, do not declare a definitive top pick. Do not combine conditional and eligible names into an unconditional ranking. Explain any weight changes requested by the user and keep the sum at 100.

An `Excluded` name has no investment-ready rank and is left out of the report. A `Conditional` name gets a provisional score only if useful and is never described as investment ready without resolving the gating unknown, and is left out of the report.
