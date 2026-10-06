---
description: Log in to Goldilocks so the investment-ready-research plugin can run
argument-hint: "[Goldilocks plugin token, e.g. gdl_pat_...]"
---

Run `scripts/goldilocks_auth.py login $ARGUMENTS` from the `screen-investment-candidates`
skill's script directory (`skills/screen-investment-candidates/scripts/goldilocks_auth.py`).

If no token was given, tell the user how to get one instead of guessing: log in to the
Goldilocks web app, open account settings, and generate a plugin access token there. Do not
accept or store anything that doesn't start with `gdl_pat_`.

Report whether login succeeded or failed based on the script's output and exit code. Never
print the raw token back to the user, and never fabricate a success if the script failed or
if Goldilocks could not be reached.
