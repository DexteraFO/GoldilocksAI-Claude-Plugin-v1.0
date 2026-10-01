# Diagram rules

Use Mermaid `flowchart LR`. Validate syntax before delivering (use a Mermaid render tool when available).

## Screening flow

```mermaid
flowchart LR
  M["Mandate criteria"] --> W["Watchlist"]
  W --> S["Screened shortlist: N names"]
  S --> L["Leading company: Name"]
  S --> X["Conditional or excluded: N names"]
```

Use real counts. If no leader is supported by the evidence, use `L["No definitive leader"]`.

## Mock relationship path

```mermaid
flowchart LR
  A["Your team"] -. "unverified / hypothetical" .-> B["Potential sector intermediary"]
  B -. "unverified / hypothetical" .-> C["Target executive: Company"]
  classDef mock stroke-dasharray: 5 5,stroke:#c79642
  class A,B,C mock
```

Rules:

- Keep the generic role nodes. Do not name a real intermediary.
- A sourced executive name may replace the company in the last node only if it is cited elsewhere in the report. Naming someone never implies a connection.
- Every edge keeps the label `unverified / hypothetical` and a dotted line.
- Next action stays "Validate introduction route".
