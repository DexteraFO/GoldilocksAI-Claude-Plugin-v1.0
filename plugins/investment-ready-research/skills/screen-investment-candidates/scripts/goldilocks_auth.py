#!/usr/bin/env python3
"""
Goldilocks login/verify helper for the investment-ready-research plugin.

Stores a Goldilocks personal access token (gdl_pat_...) under
~/.goldilocks/credentials.json and checks it against the Goldilocks backend's
GET /auth/verify/ endpoint. The screen-investment-candidates skill must get
"valid": true from `verify` before it is allowed to run.

Usage:
  goldilocks_auth.py login <gdl_pat_token>
  goldilocks_auth.py verify
  goldilocks_auth.py logout
"""
import json
import os
import stat
import sys
import urllib.error
import urllib.request

API_BASE = os.environ.get("GOLDILOCKS_API_URL", "https://goldilocksai-be.duckdns.org/api/v1/auth")
TOKEN_PREFIX = "gdl_pat_"
CREDENTIALS_PATH = os.path.expanduser("~/.goldilocks/credentials.json")


def _verify_url():
    return f"{API_BASE.rstrip('/')}/verify/"


def _call_verify(token):
    """Returns the parsed JSON body from GET /auth/verify/. Raises RuntimeError on failure."""
    req = urllib.request.Request(_verify_url(), headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
            message = body.get("error", {}).get("message", str(e))
        except Exception:
            message = f"HTTP {e.code}"
        raise RuntimeError(message) from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"could not reach Goldilocks ({e.reason})") from e


def _save_token(token):
    os.makedirs(os.path.dirname(CREDENTIALS_PATH), exist_ok=True)
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump({"token": token}, f)
    os.chmod(CREDENTIALS_PATH, stat.S_IRUSR | stat.S_IWUSR)  # 600


def _load_token():
    if not os.path.exists(CREDENTIALS_PATH):
        return None
    try:
        with open(CREDENTIALS_PATH) as f:
            return json.load(f).get("token")
    except (json.JSONDecodeError, OSError):
        return None


def login(token):
    token = token.strip()
    if not token.startswith(TOKEN_PREFIX):
        print(
            f"That doesn't look like a Goldilocks plugin token (should start with {TOKEN_PREFIX}).",
            file=sys.stderr,
        )
        return 1
    try:
        result = _call_verify(token)
    except RuntimeError as e:
        print(f"Login failed: {e}", file=sys.stderr)
        return 1
    _save_token(token)
    user = result.get("user", {})
    print(f"Logged in to Goldilocks as {user.get('email', 'unknown user')}.")
    return 0


def verify():
    token = _load_token()
    if not token:
        print(json.dumps({"valid": False, "reason": "not_logged_in"}))
        return 1
    try:
        result = _call_verify(token)
    except RuntimeError as e:
        print(json.dumps({"valid": False, "reason": str(e)}))
        return 1
    print(json.dumps(result))
    return 0 if result.get("valid") else 1


def logout():
    if os.path.exists(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)
    print("Logged out of Goldilocks.")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    command = argv[1]
    if command == "login":
        if len(argv) < 3:
            print("Usage: goldilocks_auth.py login <gdl_pat_token>", file=sys.stderr)
            return 1
        return login(argv[2])
    if command == "verify":
        return verify()
    if command == "logout":
        return logout()
    print(f"Unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
