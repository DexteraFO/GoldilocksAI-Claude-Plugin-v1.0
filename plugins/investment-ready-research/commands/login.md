---
description: Connect your Goldilocks account so the investment-ready-research plugin can run
---

Goldilocks sign-in happens through the plugin's **Goldilocks connector**, not in this chat.
Never ask the user for a password or token.

First call the Goldilocks connector's `whoami` tool.

- If it returns `"valid": true`, tell the user they're already connected and show the email it
  returned.
- Otherwise, tell them how to connect:
  - **Claude Desktop / claude.ai / Cowork:** Customize → Plugins → Investment Ready Research →
    Connectors → **Connect**. A browser window opens: sign in with LinkedIn (or their Goldilocks
    email and password), then click **Allow**.
  - **Claude Code:** run `/mcp`, choose `goldilocks`, then **Authenticate**.
  - They need an existing Goldilocks account; if they don't have one, they sign up at
    https://goldilocksai-demo.privatedns.org/ first.

Report only what the tool actually returned. If Goldilocks couldn't be reached, say so.
