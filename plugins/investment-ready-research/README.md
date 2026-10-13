# Investment Ready Research

A Claude plugin that screens companies against an investor mandate using Goldilocks company data and current public sources, and produces an evidence-backed, scored shortlist.

## What it does

- Turns a mandate (sector, geography, size band, transaction type, exclusions) into hard gates and preferences
- Builds and checks a watchlist from current public sources
- Scores each company on a 100-point mandate fit scorecard, with evidence coverage and score intervals
- Writes a report: one or two line mandate, ranked shortlist, leading company profile, thesis insights, countercase, diligence questions
- Optionally renders a self-contained HTML report that follows light/dark mode, with the mock relationship diagram bundled to work offline, and buttons to download it as a Word document or save it as PDF
- Puts the Dextera logo (`skills/screen-investment-candidates/assets/logo.jpg`) at the top of every report
- Shows progress while it works: Evaluating Goldilocks data, Evaluating existing publicly available data, Analysing and creating report, Report is successful

## Connect Goldilocks (required)

The plugin includes a **Goldilocks connector** (MCP server at
`https://goldilocksai-be.duckdns.org/mcp`). It won't run until you connect your Goldilocks account:

- **Claude Desktop / claude.ai / Cowork:** Customize → Plugins → Investment Ready Research →
  Connectors → **Connect**. Sign in with LinkedIn (or your Goldilocks email and password) and click **Allow**.
- **Claude Code:** run `/mcp`, choose `goldilocks`, then **Authenticate**.

You need an existing Goldilocks account (sign up at https://goldilocksai.privatedns.org/).
`/investment-ready-research:login` shows these steps and confirms who you're connected as;
`/investment-ready-research:logout` explains how to disconnect. No password or token is ever
typed into the chat.

Every screening run first checks the connection (`whoami`), then pulls matching companies from
Goldilocks (`search_goldilocks_companies`) before researching public sources.

## Use

Ask Claude something like: "Screen investment candidates for Indian B2B SaaS companies, revenue $5M to $50M, growth equity, as of today." The `screen-investment-candidates` skill runs automatically, or start it with `/investment-ready-research:screen`.

## Limits

Goldilocks company data plus public sources. No CRM or verified social graph. The relationship path is always a labelled mock. This is research support, not investment advice.

## Contents

- `commands/screen.md`: the slash command
- `.mcp.json`: the Goldilocks connector (remote MCP server, OAuth sign-in)
- `commands/login.md`, `commands/logout.md`: how to connect / disconnect Goldilocks
- `skills/screen-investment-candidates/SKILL.md`: workflow and evidence rules
- `references/`: research protocol, scorecard, report format
- `scripts/render_report.py`: HTML renderer (Python standard library only)
- `scripts/vendor/mermaid.min.js`: bundled Mermaid library (MIT license in `MERMAID-LICENSE`)
- `references/diagrams.md`: Mermaid diagram rules
- `examples/sample-report.json`: fictional input shape for the renderer
