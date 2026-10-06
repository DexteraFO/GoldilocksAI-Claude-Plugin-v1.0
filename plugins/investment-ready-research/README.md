# Investment Ready Research

A Claude plugin that screens companies against an investor mandate using public sources only and produces an evidence-backed, scored shortlist.

## What it does

- Turns a mandate (sector, geography, size band, transaction type, exclusions) into hard gates and preferences
- Builds and checks a watchlist from current public sources
- Scores each company on a 100-point mandate fit scorecard, with evidence coverage and score intervals
- Writes a report: one or two line mandate, ranked shortlist, leading company profile, thesis insights, countercase, diligence questions
- Optionally renders a self-contained HTML report that follows light/dark mode, with the mock relationship diagram bundled to work offline, and buttons to download it as a Word document or save it as PDF
- Puts the Dextera logo (`skills/screen-investment-candidates/assets/logo.jpg`) at the top of every report
- Shows progress while it works: Evaluating Goldilocks data, Evaluating existing publicly available data, Analysing and creating report, Report is successful

## Login required

This plugin requires a Goldilocks login before it will run. One-time setup:

1. Log in to the Goldilocks web app and generate a plugin access token from account settings.
2. Run `/investment-ready-research:login <token>` (token starts with `gdl_pat_`).
3. Run `/investment-ready-research:logout` any time to remove the stored token.

Every `/investment-ready-research:screen` run re-checks the stored token against Goldilocks
before doing anything else; it refuses to run without a valid, unexpired, unrevoked token.

## Use

Ask Claude something like: "Screen investment candidates for Indian B2B SaaS companies, revenue $5M to $50M, growth equity, as of today." The `screen-investment-candidates` skill runs automatically, or start it with `/investment-ready-research:screen`.

## Limits

Public data only. No CRM, private data or verified social graph. The relationship path is always a labelled mock. This is research support, not investment advice.

## Contents

- `commands/screen.md`: the slash command
- `commands/login.md`, `commands/logout.md`: Goldilocks login/logout commands
- `skills/screen-investment-candidates/scripts/goldilocks_auth.py`: login/verify/logout helper (stdlib only)
- `skills/screen-investment-candidates/SKILL.md`: workflow and evidence rules
- `references/`: research protocol, scorecard, report format
- `scripts/render_report.py`: HTML renderer (Python standard library only)
- `scripts/vendor/mermaid.min.js`: bundled Mermaid library (MIT license in `MERMAID-LICENSE`)
- `references/diagrams.md`: Mermaid diagram rules
- `examples/sample-report.json`: fictional input shape for the renderer
