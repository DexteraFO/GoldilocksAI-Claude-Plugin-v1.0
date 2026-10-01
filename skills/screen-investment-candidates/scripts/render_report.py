#!/usr/bin/env python3
"""Render a public-source investment report JSON as a standalone HTML file."""

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def esc(value):
    return html.escape(str(value if value is not None else "Unknown"), quote=True)


def safe_url(value):
    parsed = urlparse(str(value or ""))
    return value if parsed.scheme == "https" and parsed.netloc else ""


def cite_text(value):
    """Escape text and turn [S1] references into local source links."""
    escaped = esc(value)
    return re.sub(r"\[(S\d+)\]", r'<a class="cite" href="#source-\1">[\1]</a>', escaped)


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("The report must be a JSON object")
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    if any(not isinstance(s, dict) for s in sources):
        raise ValueError("Every source must be an object")
    for c in data.get("candidates", []):
        if not isinstance(c, dict) or not isinstance(c.get("sources", []), list):
            raise ValueError("Each candidate must be an object with a list of sources")
    ids = [s.get("id") for s in sources]
    if any(not re.fullmatch(r"S\d+", str(i or "")) for i in ids) or len(ids) != len(set(ids)):
        raise ValueError("Source IDs must be unique S1, S2, ... identifiers")
    if any(not safe_url(s.get("url")) for s in sources):
        raise ValueError("Every source needs a valid HTTPS URL")
    used = set(re.findall(r"\[(S\d+)\]", json.dumps(data, ensure_ascii=False)))
    used.update(i for c in data.get("candidates", []) for i in c.get("sources", []))
    missing = used - set(ids)
    if missing:
        raise ValueError(f"Missing source records: {', '.join(sorted(missing))}")
    for key in ("mandate", "candidates", "conditional_excluded"):
        if not isinstance(data.get(key, []), list):
            raise ValueError(f"{key} must be a list")
    if data.get("leader") is not None and not isinstance(data["leader"], dict):
        raise ValueError("leader must be an object when present")


def table(headers, rows):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def list_items(items):
    return "<ul>" + "".join(f"<li>{cite_text(item)}</li>" for item in items) + "</ul>"


def render(data):
    validate(data)
    mandate = table(
        ["Criterion", "Requirement", "Type"],
        [[esc(x.get("criterion", "")), cite_text(x.get("requirement", "")), esc(x.get("type", ""))]
         for x in data.get("mandate", [])],
    )
    candidates = data.get("candidates", [])
    rows = []
    for index, item in enumerate(candidates, 1):
        ref = " ".join(f'<a class="cite" href="#source-{esc(s)}">[{esc(s)}]</a>' for s in item.get("sources", []))
        rows.append([
            f'<span class="score">{esc(item.get("score", "Unscored"))}</span><small>#{index} · {esc(item.get("coverage", "Unknown"))} coverage</small>',
            f'<strong>{esc(item.get("company", "Unknown"))}</strong><small>{esc(item.get("eligibility", "Unknown"))}</small>',
            esc(item.get("location", "Unknown")), esc(item.get("revenue", "Unknown")),
            esc(item.get("employees", "Unknown")), esc(item.get("ownership", "Unknown")),
            f'{cite_text(item.get("signal", "Unknown"))}<small>{ref}</small>',
            esc(item.get("ceo", "Unknown")), esc(item.get("action", "Review")),
        ])
    shortlist = table(["Rank / fit", "Company", "Location", "Revenue", "Employees", "Ownership", "Public signal", "CEO", "Next action"], rows)
    leader = data.get("leader")
    profile = '<p class="muted">No definitive leading company is supported by the available evidence.</p>'
    if leader:
        site = safe_url(leader.get("website"))
        site_html = f'<a href="{esc(site)}" target="_blank" rel="noopener noreferrer">{esc(urlparse(site).netloc)}</a>' if site else ""
        tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in leader.get("tags", []))
        metrics = "".join(f'<div class="metric"><small>{esc(m.get("label", ""))}</small><b>{esc(m.get("value", "Unknown"))}</b></div>' for m in leader.get("metrics", []))
        details = table(["Dimension", "Points", "Rationale"], [
            [esc(x.get("dimension", "")), esc(x.get("points", "Unknown")), cite_text(x.get("rationale", ""))]
            for x in leader.get("score_details", [])
        ])
        profile = f'''
          <section class="panel">
            <div class="profile-head"><div><h3>{esc(leader.get("company", "Unknown"))}</h3><p>{site_html}</p></div>
              <span class="badge">Mandate fit: {esc(leader.get("score", "Unscored"))}</span></div>
            <div class="tags">{tags}</div><div class="metric-grid">{metrics}</div>
          </section>
          <section><h3>Key investment insights</h3>{list_items(leader.get("insights", []))}</section>
          <section><h3>Company overview</h3><p>{cite_text(leader.get("overview", "Unknown"))}</p></section>
          <div class="two-col"><section><h3>Countercase</h3><p>{cite_text(leader.get("countercase", "Unknown"))}</p></section>
            <section><h3>Diligence questions</h3>{list_items(leader.get("diligence", []))}</section></div>
          <section><h3>Scoring details</h3>{details}</section>
        '''
    excluded = data.get("conditional_excluded", [])
    excluded_html = table(["Company", "Status", "Reason"], [[esc(x.get("company", "")), esc(x.get("status", "")), cite_text(x.get("reason", ""))] for x in excluded]) if excluded else "<p>None listed.</p>"
    sources_html = "".join(
        f'<li id="source-{esc(x["id"])}"><strong>[{esc(x["id"])}] {esc(x.get("title", "Untitled"))}</strong>, '
        f'{esc(x.get("publisher", "Unknown publisher"))}, {esc(x.get("date", "undated"))}; accessed {esc(x.get("accessed", "Unknown"))}. '
        f'<a href="{esc(x["url"])}" target="_blank" rel="noopener noreferrer">Open source</a></li>'
        for x in data.get("sources", [])
    )
    css = '''
      :root{color-scheme:dark;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;background:#0d151e;color:#f4f6f8}
      *{box-sizing:border-box}body{margin:0;line-height:1.55}main{max-width:1280px;margin:auto;padding:30px 20px 72px}
      header{border-bottom:1px solid #263340;padding-bottom:22px;margin-bottom:28px}.eyebrow{color:#d6a843;letter-spacing:.12em;text-transform:uppercase;font-size:12px;font-weight:800}
      h1{font-size:clamp(27px,3vw,40px);line-height:1.15;margin:8px 0}h2{font-size:21px;margin:36px 0 14px}h3{font-size:18px;margin:0 0 12px}
      p{color:#c5ced8;margin:8px 0 12px}.muted,small{color:#98a6b7}small{display:block;font-size:12px;margin-top:5px}
      a{color:#d7b263;text-decoration:none}a:hover{text-decoration:underline}.cite{white-space:nowrap;font-size:.9em}
      .panel{background:#192331;border:1px solid #2d3a47;border-radius:16px;padding:24px}.table-wrap{overflow-x:auto;border:1px solid #2a3643;border-radius:15px}
      table{border-collapse:collapse;min-width:780px;width:100%;background:#151d28}th{text-align:left;background:#1b2635;color:#b8c5d3;text-transform:uppercase;font-size:11px;letter-spacing:.06em}
      th,td{padding:13px 14px;border-bottom:1px solid #2b3541;vertical-align:top;font-size:13px}tr:last-child td{border-bottom:0}strong,b{color:#f6f7fa}
      .score,.badge{display:inline-block;background:#17392f;color:#54e795;border:1px solid #23644d;border-radius:20px;padding:4px 9px;font-weight:800;white-space:nowrap}
      .profile-head{display:flex;justify-content:space-between;gap:15px;align-items:flex-start;flex-wrap:wrap}.profile-head h3{font-size:25px;margin:0}
      .tags{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 18px}.tag{border:1px solid #736035;color:#f5bd4b;border-radius:20px;padding:5px 10px;font-size:12px}
      .metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.metric{border:1px solid #303944;border-radius:14px;background:#151e29;padding:15px}
      .metric small{text-transform:uppercase;letter-spacing:.07em;font-weight:700}.metric b{display:block;font-size:17px;margin-top:7px}.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
      section{margin-top:27px}ul{padding-left:22px}li{margin:9px 0;color:#d4dce5}li::marker{color:#d2ab57}
      .mock{border:1px solid #6b5a35;background:#242519;border-radius:16px;padding:18px}.mock strong{color:#f3ca73}.route{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0}
      .node{border:1px solid #536071;border-radius:12px;padding:10px 13px;background:#1a2430}.edge{color:#f1bb59;font-size:12px;border-bottom:2px dashed #c79642;padding:0 8px 4px}
      .footnote{font-size:12px;color:#9facb9}.sources{word-break:break-word}
      @media(max-width:720px){main{padding:20px 12px 60px}.metric-grid{grid-template-columns:repeat(2,1fr)}.two-col{grid-template-columns:1fr}.route{flex-direction:column;align-items:stretch}.edge{text-align:center}}
    '''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{esc(data.get("title", "Investment Ready Recommendations"))}</title><style>{css}</style></head><body><main>
    <header><div class="eyebrow">Public-source company summary report</div><h1>{esc(data.get("title", "Investment Ready Recommendations"))}</h1>
      <p>As of {esc(data.get("as_of", "Unknown"))} · Public data only · Relationship route is illustrative</p><p>{cite_text(data.get("summary", ""))}</p></header>
    <section><h2>Investment mandate</h2>{mandate}</section><section><h2>Ranked shortlist</h2>{shortlist}</section>
    <section><h2>Leading company</h2>{profile}</section>
    <section><h2>Relationship path, MOCK ONLY</h2><div class="mock"><strong>Illustrative route, no verified connections</strong>
      <div class="route"><span class="node">Your team</span><span class="edge">unverified / hypothetical →</span>
      <span class="node">Potential sector intermediary</span><span class="edge">unverified / hypothetical →</span>
      <span class="node">Target executive</span></div><p>Next action: Validate introduction route. This diagram does not establish any mutual contact or warm introduction.</p></div></section>
    <section><h2>Conditional and excluded names</h2>{excluded_html}</section>
    <section class="sources"><h2>Sources</h2><ol>{sources_html}</ol></section>
    <p class="footnote">Scores measure mandate fit from available evidence. They are not predicted returns or investment advice.</p>
    </main></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_html.write_text(render(data), encoding="utf-8")


if __name__ == "__main__":
    main()
