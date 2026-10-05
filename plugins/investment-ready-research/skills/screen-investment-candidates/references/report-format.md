# Report format

## Markdown output order

1. `Investment Ready Recommendations` with as-of date and a one-paragraph strategic summary.
2. `Investment mandate`: a one or two line summary of the criteria. No table.
3. `Ranked shortlist` table: rank/fit interval, company, location, revenue + year, employees + date, ownership/status, public signal, CEO + date, eligibility, next action. Add evidence coverage in each row. If a field is unavailable, write Unknown.
4. `Leading company` profile with sector tags and six metric cards: annual revenue, employees, founded, ownership, growth, funding. Omit or mark unknown without filler values.
5. `Key investment insights` of 3–5 bullets, each tying a source-backed fact to the mandate and showing an inference as inference.
6. `Company overview`, `Countercase`, and `Diligence questions`.
7. `Relationship path, mock only`, displaying generic roles linked by **unverified hypothetical** edges. If a sourced executive is named, that confirms identity only, not the connection. Next action: Validate introduction route. Show it as the Mermaid diagram from [diagrams.md](diagrams.md).
8. `Scoring details` (six dimensions, points, rationale).

Do not output a screening flow diagram, a conditional/excluded names section, or a sources list. Keep the evidence ledger in your own working notes and share it if asked.

This plugin has no "Handshake" action and no proprietary score name. Use "Validate introduction route" and "Mandate fit score." Do not present CRM columns or hidden internal validation.

## Optional HTML artifact

If Claude can execute scripts, write UTF-8 JSON to a workspace path and run:

`python3 scripts/render_report.py input.json output.html`

Locate the script relative to this skill's directory. The script uses Python standard library only and inlines the bundled Mermaid library (`scripts/vendor/mermaid.min.js`), so the relationship path diagram renders without internet access. If the bundle is missing it falls back to a CDN. It escapes untrusted text and renders a responsive report that follows the viewer's light/dark setting (with a manual toggle), readable dark text on light backgrounds, and a closing toolbar to download the report as a Word document or save it as PDF. File creation depends on the Claude environment; the Markdown report remains the baseline.

The JSON object has the following shape (strings may be empty/`Unknown`, but do not silently invent them):

```json
{
  "title": "Investment Ready Recommendations",
  "as_of": "2026-09-29",
  "summary": "Mandate-specific conclusion, including limitations.",
  "mandate": "One or two lines: sector, geography, size band, deal type, key exclusions.",
  "candidates": [{
    "company":"Example Company", "score":"62–82/100 provisional", "coverage":"80%",
    "location":"City, Country", "revenue":"Unknown", "employees":"Unknown",
    "ownership":"Private; verify", "signal":"Specific public signal",
    "ceo":"Unknown", "eligibility":"Conditional", "action":"Validate eligibility"
  }],
  "leader": {
    "company":"Example Company", "website":"https://example.org", "score":"62–82/100 provisional",
    "tags":["Category"],
    "metrics":[{"label":"Annual revenue", "value":"Unknown"}],
    "insights":["Source-backed fact → explained thesis implication."],
    "overview":"Dated summary.",
    "countercase":"The strongest reason the thesis may fail.",
    "diligence":["A question that would resolve a material uncertainty."],
    "score_details":[{"dimension":"Sector/product fit", "points":"15/20", "rationale":"Evidence"}]
  }
}
```

This is a shape example with fictional placeholders, not a research result. The renderer always labels the relationship panel as mock and supplies generic route nodes itself; JSON cannot assert a real connection. `leader` may be omitted if evidence is insufficient. `[S1]`-style markers and any `sources` or `conditional_excluded` keys are ignored by the renderer; they are never displayed.
