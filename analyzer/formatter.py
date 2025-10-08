# -*- coding: utf-8 -*-
def result_to_html_table(result_text: str) -> str:
    pairs = []
    for line in (ln.strip() for ln in result_text.splitlines()):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        pairs.append((k.strip(), v.strip()))

    def badge_html(value: str) -> str:
        low = any(w in value for w in ["낮음", "low"])
        mid = any(w in value for w in ["보통", "중간", "medium"])
        high = any(w in value for w in ["높음", "high"])
        cls = "badge-mid"
        if low: cls = "badge-low"
        if high: cls = "badge-high"
        return f'<span class="badge {cls}">{value}</span>'

    rows_html = []
    for idx, (k, v) in enumerate(pairs, 1):
        if "위험도" in k:
            v = badge_html(v)
        rows_html.append(f"<tr><td class='idx'>{idx}</td><td class='key'>{k}</td><td class='val'>{v}</td></tr>")

    return f"""
<html>
<head>
<meta charset="utf-8"/>
<style>
:root {{
  --bg:#fff; --line:#e5e7eb; --low:#16a34a; --mid:#f59e0b; --high:#ef4444;
}}
table.anatable {{ width:100%; border-collapse:collapse; font-size:15px; }}
th,td {{ padding:10px; border-bottom:1px solid var(--line); }}
.idx {{ width:40px; text-align:center; color:#6b7280; }}
.key {{ width:220px; font-weight:700; white-space:nowrap; }}
.badge {{ padding:3px 8px; border-radius:8px; font-weight:700; font-size:13px; }}
.badge-low {{ background:rgba(22,163,74,.1); color:var(--low); }}
.badge-mid {{ background:rgba(245,158,11,.1); color:var(--mid); }}
.badge-high {{ background:rgba(239,68,68,.1); color:var(--high); }}
</style>
</head>
<body>
<table class="anatable">
<thead><tr><th>#</th><th>항목</th><th>분석 결과</th></tr></thead>
<tbody>
{''.join(rows_html)}
</tbody>
</table>
</body>
</html>
"""
