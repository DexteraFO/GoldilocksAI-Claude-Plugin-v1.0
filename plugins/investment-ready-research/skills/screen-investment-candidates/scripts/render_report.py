#!/usr/bin/env python3
"""Render a public-source investment report JSON as a standalone HTML file.

The report follows the viewer's light/dark setting (prefers-color-scheme), has a
manual theme toggle, and ends with buttons to save it as a Word document or PDF.
"""

import argparse
import base64
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


def clean(value):
    """Escape text and drop [S1]-style source markers (the report shows no source list)."""
    return re.sub(r"\s*\[S\d+\]", "", esc(value))


def mermaid_loader():
    """Inline the bundled Mermaid library when present, else load it from a CDN."""
    bundled = Path(__file__).parent / "vendor" / "mermaid.min.js"
    if bundled.exists():
        code = bundled.read_text(encoding="utf-8").replace("</script", "<\\/script")
        return f"<script>{code}</script>"
    return '<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'


def logo_html():
    """Embed the brand logo (assets/logo.jpg) so every report carries it and stays self-contained."""
    logo = Path(__file__).parent.parent / "assets" / "logo.jpg"
    if not logo.exists():
        raise FileNotFoundError(f"Brand logo missing: {logo}. Every report must include it.")
    encoded = base64.b64encode(logo.read_bytes()).decode("ascii")
    return f'<img class="logo" alt="Dextera logo" width="132" height="110" src="data:image/jpeg;base64,{encoded}">'


def mm(value, limit=60):
    """Make text safe for a quoted Mermaid label."""
    cleaned = re.sub(r"[^A-Za-z0-9 .,&/+-]", "", str(value if value is not None else ""))
    return cleaned.strip()[:limit] or "Unknown"


def relationship_diagram(data):
    leader = data.get("leader") or {}
    target = mm(leader.get("company", "")) if leader else "Unknown"
    return "\n".join([
        "flowchart LR",
        '  A["Your team"] -. "unverified / hypothetical" .-> B["Potential sector intermediary"]',
        f'  B -. "unverified / hypothetical" .-> C["Target executive: {target}"]',
        "  classDef mock stroke-dasharray: 5 5,stroke:#c79642",
        "  class A,B,C mock",
    ])


def mandate_text(data):
    """The mandate is a one or two line summary. Older list-shaped input is flattened."""
    mandate = data.get("mandate", "")
    if isinstance(mandate, list):
        parts = [f'{x.get("criterion", "")}: {x.get("requirement", "")}' for x in mandate if isinstance(x, dict)]
        return "; ".join(p for p in parts if p.strip(": "))
    return str(mandate or "")


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("The report must be a JSON object")
    if not isinstance(data.get("mandate", ""), (str, list)):
        raise ValueError("mandate must be a short string")
    if not isinstance(data.get("candidates", []), list) or any(not isinstance(c, dict) for c in data.get("candidates", [])):
        raise ValueError("candidates must be a list of objects")
    if data.get("leader") is not None and not isinstance(data["leader"], dict):
        raise ValueError("leader must be an object when present")


def table(headers, rows):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def list_items(items):
    return "<ul>" + "".join(f"<li>{clean(item)}</li>" for item in items) + "</ul>"


CSS = '''
:root{color-scheme:light;--bg:#f6f7f9;--text:#18212e;--muted:#4a5666;--panel:#ffffff;--panel2:#f0f3f7;--border:#cfd7e1;
  --th:#e8edf3;--thtext:#243246;--link:#0b5cad;--accent:#8a5a00;--badge-bg:#e1f4ea;--badge-text:#0d5f38;--badge-border:#9bd2b4;
  --tag-border:#b58a2a;--tag-text:#6e4a00;--mock-bg:#fff7e0;--mock-border:#dcbd72;--edge:#8a5a00}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#0d151e;--text:#f1f4f8;--muted:#b3bfce;--panel:#192331;--panel2:#151d28;
  --border:#2d3a47;--th:#1b2635;--thtext:#d3deea;--link:#e0bb6a;--accent:#e0bb6a;--badge-bg:#17392f;--badge-text:#5cf0a0;--badge-border:#23644d;
  --tag-border:#736035;--tag-text:#f5bd4b;--mock-bg:#242519;--mock-border:#6b5a35;--edge:#f1bb59}}
:root[data-theme=dark]{color-scheme:dark;--bg:#0d151e;--text:#f1f4f8;--muted:#b3bfce;--panel:#192331;--panel2:#151d28;
  --border:#2d3a47;--th:#1b2635;--thtext:#d3deea;--link:#e0bb6a;--accent:#e0bb6a;--badge-bg:#17392f;--badge-text:#5cf0a0;--badge-border:#23644d;
  --tag-border:#736035;--tag-text:#f5bd4b;--mock-bg:#242519;--mock-border:#6b5a35;--edge:#f1bb59}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;line-height:1.55;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--text)}
main{max-width:1280px;margin:auto;padding:30px 20px 72px}
header{border-bottom:1px solid var(--border);padding-bottom:22px;margin-bottom:28px}
.logo{display:block;width:132px;height:auto;border-radius:12px;margin-bottom:18px}
.eyebrow{color:var(--accent);letter-spacing:.12em;text-transform:uppercase;font-size:12px;font-weight:800}
h1{font-size:clamp(27px,3vw,40px);line-height:1.15;margin:8px 0;color:var(--text)}
h2{font-size:21px;margin:36px 0 14px;color:var(--text)}h3{font-size:18px;margin:0 0 12px;color:var(--text)}
p,li,td,strong,b{color:var(--text)}
.muted,small{color:var(--muted)}small{display:block;font-size:12px;margin-top:5px}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
.panel{background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:24px}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:15px}
table{border-collapse:collapse;min-width:780px;width:100%;background:var(--panel)}
th{text-align:left;background:var(--th);color:var(--thtext);text-transform:uppercase;font-size:11px;letter-spacing:.06em}
th,td{padding:13px 14px;border-bottom:1px solid var(--border);vertical-align:top;font-size:13px}tr:last-child td{border-bottom:0}
.score,.badge{display:inline-block;background:var(--badge-bg);color:var(--badge-text);border:1px solid var(--badge-border);border-radius:20px;padding:4px 9px;font-weight:800;white-space:nowrap}
.profile-head{display:flex;justify-content:space-between;gap:15px;align-items:flex-start;flex-wrap:wrap}.profile-head h3{font-size:25px;margin:0}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 18px}.tag{border:1px solid var(--tag-border);color:var(--tag-text);border-radius:20px;padding:5px 10px;font-size:12px}
.metric-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.metric{border:1px solid var(--border);border-radius:14px;background:var(--panel2);padding:15px}
.metric small{text-transform:uppercase;letter-spacing:.07em;font-weight:700}.metric b{display:block;font-size:17px;margin-top:7px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
section{margin-top:27px}ul{padding-left:22px}li{margin:9px 0}li::marker{color:var(--accent)}
.mandate{font-size:15px;margin:0}
.mock{border:1px solid var(--mock-border);background:var(--mock-bg);border-radius:16px;padding:18px}
.route{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0}
.node{border:1px solid var(--border);border-radius:12px;padding:10px 13px;background:var(--panel);color:var(--text)}
.edge{color:var(--edge);font-size:12px;border-bottom:2px dashed var(--mock-border);padding:0 8px 4px}
pre.mermaid{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:16px;overflow-x:auto;color:var(--muted);font-size:12px;white-space:pre-wrap}
pre.mermaid[data-processed]{white-space:normal;color:inherit}
.footnote{font-size:12px;color:var(--muted)}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:40px;padding:18px;border:1px solid var(--border);border-radius:16px;background:var(--panel)}
.toolbar strong{margin-right:auto}
button{font:inherit;font-size:14px;font-weight:700;cursor:pointer;color:var(--text);background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:9px 14px}
button.primary{background:var(--link);color:#fff;border-color:var(--link)}
button:hover{filter:brightness(.96)}
.theme-btn{position:fixed;top:12px;right:12px;z-index:5}
@media(max-width:720px){main{padding:20px 12px 60px}.metric-grid{grid-template-columns:repeat(2,1fr)}.two-col{grid-template-columns:1fr}.route{flex-direction:column;align-items:stretch}.edge{text-align:center}}
@media print{:root{color-scheme:light;--bg:#fff;--text:#000;--muted:#333;--panel:#fff;--panel2:#fff;--border:#999;--th:#eee;--thtext:#000;--link:#000}
  .no-doc,.theme-btn{display:none!important}main{padding:0}table{min-width:0}.table-wrap{overflow:visible}}
'''

SCRIPT = '''
(function () {
  var root = document.documentElement;
  function dark() {
    var t = root.getAttribute("data-theme");
    return t ? t === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  var diagrams = Array.prototype.map.call(document.querySelectorAll("pre.mermaid"), function (el) {
    return {el: el, src: el.textContent};
  });
  async function draw() {
    try {
      if (!window.mermaid) return;
      mermaid.initialize({startOnLoad: false, theme: dark() ? "dark" : "default", securityLevel: "strict"});
      diagrams.forEach(function (d) { d.el.removeAttribute("data-processed"); d.el.textContent = d.src; });
      await mermaid.run({querySelector: ".mermaid"});
      var route = document.querySelector(".route");
      if (route) route.style.display = "none";
    } catch (e) { /* keep static route visible */ }
  }
  function label() { document.getElementById("theme-btn").textContent = dark() ? "Light mode" : "Dark mode"; }
  document.getElementById("theme-btn").addEventListener("click", function () {
    root.setAttribute("data-theme", dark() ? "light" : "dark");
    label(); draw();
  });
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
      if (!root.getAttribute("data-theme")) { label(); draw(); }
    });
  }
  label(); draw();

  document.getElementById("pdf-btn").addEventListener("click", function () { window.print(); });
  document.getElementById("doc-btn").addEventListener("click", function () {
    var copy = document.querySelector("main").cloneNode(true);
    copy.querySelectorAll(".no-doc,pre.mermaid").forEach(function (n) { n.remove(); });
    var route = copy.querySelector(".route");
    if (route) route.style.display = "block";
    var style = "body{font-family:Calibri,Arial,sans-serif;color:#000;background:#fff}" +
      "table{border-collapse:collapse;width:100%}th,td{border:1px solid #999;padding:5px;font-size:10pt;vertical-align:top;color:#000}" +
      "th{background:#e8edf3}h1,h2,h3,p,li,small{color:#000}small{display:block}a{color:#0b5cad}" +
      ".node{border:1px solid #999;padding:3px 6px}.edge{color:#8a5a00}.tag{border:1px solid #b58a2a;padding:1px 6px}" +
      ".metric{display:inline-block;border:1px solid #999;padding:6px;margin:3px}";
    var doc = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" ' +
      'xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8"><title>' + document.title +
      "</title><style>" + style + "</style></head><body>" + copy.innerHTML + "</body></html>";
    var blob = new Blob(["\\ufeff", doc], {type: "application/msword"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = (document.title || "investment-report").replace(/[^A-Za-z0-9 _-]/g, "").trim().replace(/ +/g, "-") + ".doc";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });
})();
'''


def render(data):
    validate(data)
    title = esc(data.get("title", "Investment Ready Recommendations"))
    mandate = f'<p class="mandate">{clean(mandate_text(data)) or "Not specified."}</p>'

    rows = []
    for index, item in enumerate(data.get("candidates", []), 1):
        rows.append([
            f'<span class="score">{esc(item.get("score", "Unscored"))}</span><small>#{index} · {esc(item.get("coverage", "Unknown"))} coverage</small>',
            f'<strong>{esc(item.get("company", "Unknown"))}</strong><small>{esc(item.get("eligibility", "Unknown"))}</small>',
            esc(item.get("location", "Unknown")), esc(item.get("revenue", "Unknown")),
            esc(item.get("employees", "Unknown")), esc(item.get("ownership", "Unknown")),
            clean(item.get("signal", "Unknown")),
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
            [esc(x.get("dimension", "")), esc(x.get("points", "Unknown")), clean(x.get("rationale", ""))]
            for x in leader.get("score_details", [])
        ])
        profile = f'''
          <section class="panel">
            <div class="profile-head"><div><h3>{esc(leader.get("company", "Unknown"))}</h3><p>{site_html}</p></div>
              <span class="badge">Mandate fit: {esc(leader.get("score", "Unscored"))}</span></div>
            <div class="tags">{tags}</div><div class="metric-grid">{metrics}</div>
          </section>
          <section><h3>Key investment insights</h3>{list_items(leader.get("insights", []))}</section>
          <section><h3>Company overview</h3><p>{clean(leader.get("overview", "Unknown"))}</p></section>
          <div class="two-col"><section><h3>Countercase</h3><p>{clean(leader.get("countercase", "Unknown"))}</p></section>
            <section><h3>Diligence questions</h3>{list_items(leader.get("diligence", []))}</section></div>
          <section><h3>Scoring details</h3>{details}</section>
        '''

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><title>{title}</title><style>{CSS}</style></head><body>
<button class="theme-btn no-doc" id="theme-btn" type="button">Dark mode</button>
<main>
<header>{logo_html()}<div class="eyebrow">Public-source company summary report</div><h1>{title}</h1>
  <p>As of {esc(data.get("as_of", "Unknown"))} · Public data only · Relationship route is illustrative</p><p>{clean(data.get("summary", ""))}</p></header>
<section><h2>Investment mandate</h2>{mandate}</section>
<section><h2>Ranked shortlist</h2>{shortlist}</section>
<section><h2>Leading company</h2>{profile}</section>
<section><h2>Relationship path, MOCK ONLY</h2><div class="mock"><strong>Illustrative route, no verified connections</strong>
  <div class="route"><span class="node">Your team</span><span class="edge">unverified / hypothetical →</span>
  <span class="node">Potential sector intermediary</span><span class="edge">unverified / hypothetical →</span>
  <span class="node">Target executive</span></div><pre class="mermaid" id="rel-diagram">{esc(relationship_diagram(data))}</pre>
  <p>Next action: Validate introduction route. This diagram does not establish any mutual contact or warm introduction.</p></div></section>
<p class="footnote">Scores measure mandate fit from available evidence. They are not predicted returns or investment advice.</p>
<div class="toolbar no-doc"><strong>Convert this report to a document</strong>
  <button class="primary" id="doc-btn" type="button">Download as Word (.doc)</button>
  <button id="pdf-btn" type="button">Save as PDF</button></div>
</main>
{mermaid_loader()}
<script>{SCRIPT}</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_html.write_text(render(data), encoding="utf-8")


if __name__ == "__main__":
    main()
