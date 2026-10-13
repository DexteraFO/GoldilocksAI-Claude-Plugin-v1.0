---
description: Screen companies against an investor mandate using Goldilocks and public data and produce a report
argument-hint: "[investment mandate, e.g. Indian B2B SaaS, $5M-$50M revenue, growth equity]"
---

Before anything else, confirm the Goldilocks connection: call the Goldilocks connector's
`whoami` tool. If it isn't available, asks for authorization, or doesn't return `"valid": true`,
stop here: do not run the skill, do not print any progress line below, and tell the user to
connect Goldilocks (run `/investment-ready-research:login` for the steps). If the error says
Goldilocks couldn't be reached, say that rather than asking them to reconnect.

Use the `screen-investment-candidates` skill to screen investment candidates for this mandate: $ARGUMENTS

If no mandate was given, ask for the few details that decide eligibility (sector, geography, size band, deal type, exclusions) before starting.

Follow the skill's "Progress messages" section exactly. Print each of these lines as its own plain-text line when that stage begins:

1. `⏳ Evaluating Goldilocks data…`
2. `⏳ Evaluating existing publicly available data…`
3. `⏳ Analysing and creating report…`
4. `✅ Report is successful.` (only once the report really exists)

Show a one or two line mandate, no screening flow, no conditional/excluded names and no sources list. Render the HTML report with `${CLAUDE_PLUGIN_ROOT}/skills/screen-investment-candidates/scripts/render_report.py` when you can run scripts, and finish by telling the user the report can be downloaded as a Word document or PDF from the buttons at the bottom, or offer to convert it.
