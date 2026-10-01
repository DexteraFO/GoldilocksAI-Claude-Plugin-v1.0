# Investment Ready Research

A Claude plugin that screens companies against an investor mandate using public sources only and produces an evidence-backed, scored shortlist.

## What it does

- Turns a mandate (sector, geography, size band, transaction type, exclusions) into hard gates and preferences
- Builds and checks a watchlist from current public sources
- Scores each company on a 100-point mandate fit scorecard, with evidence coverage and score intervals
- Writes a report: ranked shortlist, leading company profile, thesis insights, countercase, diligence questions, sources
- Optionally renders a self-contained HTML report with Mermaid diagrams (screening flow and mock relationship path), bundled so they work offline

## Use

Ask Claude something like: "Screen investment candidates for Indian B2B SaaS companies, revenue $5M to $50M, growth equity, as of today." The `screen-investment-candidates` skill runs automatically.

## Limits

Public data only. No CRM, private data or verified social graph. The relationship path is always a labelled mock. This is research support, not investment advice.

## Contents

- `skills/screen-investment-candidates/SKILL.md`: workflow and evidence rules
- `references/`: research protocol, scorecard, report format
- `scripts/render_report.py`: HTML renderer (Python standard library only)
- `scripts/vendor/mermaid.min.js`: bundled Mermaid library (MIT license in `MERMAID-LICENSE`)
- `references/diagrams.md`: Mermaid diagram rules
- `examples/sample-report.json`: fictional input shape for the renderer
