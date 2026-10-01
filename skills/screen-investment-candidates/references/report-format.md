# Report format

## Markdown output order

1. `Investment Ready Recommendations` with as-of date and a one-paragraph strategic summary.
2. `Investment mandate` table: criteria, hard/soft status, source of instruction.
3. `Ranked shortlist` table: rank/fit interval, company, location, revenue + year, employees + date, ownership/status, public signal, CEO + date, eligibility, next action. Add evidence coverage and direct source IDs in each row or a companion evidence table. If a field is unavailable, write Unknown.
4. `Leading company` profile with sector tags and six metric cards: annual revenue, employees, founded, ownership, growth, funding. Omit or mark unknown without filler values.
5. `Key investment insights` of 3–5 bullets, each tying a source-backed fact to the mandate and showing an inference as inference.
6. `Company overview`, `Countercase`, and `Diligence questions`.
7. `Relationship path, mock only`, displaying generic roles linked by **unverified hypothetical** edges. If a sourced executive is named, that confirms identity only, not the connection. Next action: Validate introduction route.
8. `Scoring details` (six dimensions, points, rationale, source IDs), `Conditional/excluded names`, and `Sources` with title, publisher, date, URL, access date. Keep the full audit trail accessible even when a compact table leads.

This plugin has no "Handshake" action and no proprietary score name. Use "Validate introduction route" and "Mandate fit score." Do not present CRM columns or hidden internal validation.

## Optional HTML artifact

If Claude can execute scripts, write UTF-8 JSON to a workspace path and run:

`python3 scripts/render_report.py input.json output.html`

Locate the script relative to this skill's directory. The script uses Python standard library only. It escapes untrusted text and renders a dark, responsive report with the same information hierarchy as the Markdown report. File creation depends on the Claude environment; the Markdown report remains the baseline.

The JSON object has the following shape (strings may be empty/`Unknown`, but do not silently invent them):

```json
{
  "title": "Investment Ready Recommendations",
  "as_of": "2026-09-29",
  "summary": "Mandate-specific conclusion, including limitations.",
  "mandate": [{"criterion":"Sector", "requirement":"Example category", "type":"Hard"}],
  "candidates": [{
    "company":"Example Company", "score":"62–82/100 provisional", "coverage":"80%",
    "location":"City, Country", "revenue":"Unknown", "employees":"Unknown",
    "ownership":"Private; verify", "signal":"Specific sourced public signal [S1]",
    "ceo":"Unknown", "eligibility":"Conditional", "action":"Validate eligibility",
    "sources":["S1"]
  }],
  "leader": {
    "company":"Example Company", "website":"https://example.org", "score":"62–82/100 provisional",
    "tags":["Category"],
    "metrics":[{"label":"Annual revenue", "value":"Unknown"}],
    "insights":["Source-backed fact [S1] → explained thesis implication."],
    "overview":"Dated summary with source IDs.",
    "countercase":"The strongest reason the thesis may fail.",
    "diligence":["A question that would resolve a material uncertainty."],
    "score_details":[{"dimension":"Sector/product fit", "points":"15/20", "rationale":"Evidence [S1]"}]
  },
  "conditional_excluded":[{"company":"Other Company", "status":"Excluded", "reason":"Specific gate failed [S2]"}],
  "sources":[{"id":"S1", "title":"Source title", "publisher":"Publisher", "date":"YYYY-MM-DD", "url":"https://example.org/path", "accessed":"2026-09-29"}]
}
```

This is a shape example with fictional placeholders, not a research result. The renderer always labels the relationship panel as mock and supplies generic route nodes itself; JSON cannot assert a real connection. `leader` may be omitted if evidence is insufficient. Sources remain in the HTML report. Any string with `[S1]` should correspond to a source item; validate references before delivery.
