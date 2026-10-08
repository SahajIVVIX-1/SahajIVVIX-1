"""Render the "Insights" board: a year of GitHub activity, drawn from the GraphQL API.

    ACCESS_TOKEN=... USER_NAME=SahajIVVIX-1 python assets/build/insights.py

Writes assets/insights-dark.svg and assets/insights-light.svg. Run by the
README build workflow; with no token it renders the empty "syncing" state.
"""
import datetime as dt
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PORTRAIT", "")  # the board has no portrait; skip loading it
from build import Svg, THEMES, OUT, measure  # noqa: E402

EXTRA = {"dark": dict(gold="#D4B06A", plum="#B48EAD"), "light": dict(gold="#8C6A1F", plum="#7A4F74")}
DIGITS = "0123456789,.%"
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions
      totalIssueContributions totalPullRequestReviewContributions
      contributionCalendar { totalContributions
        weeks { contributionDays { date contributionCount weekday contributionLevel } } }
      commitContributionsByRepository(maxRepositories: 6) {
        repository { name isPrivate } contributions { totalCount } }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""


# ── data ────────────────────────────────────────────────────────────────────
def fetch(login, token):
    import requests
    r = requests.post("https://api.github.com/graphql", json={"query": QUERY, "variables": {"login": login}},
                      headers={"authorization": f"token {token}"}, timeout=30)
    r.raise_for_status()
    body = r.json()
    if body.get("errors") or not (body.get("data") or {}).get("user"):
        raise RuntimeError(json.dumps(body.get("errors"))[:300])
    return body["data"]["user"]


def digest(user):
    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1  # today may not have started yet
    while i >= 0 and counts[i]:
        cur += 1; i -= 1
    busiest = max(days, key=lambda d: d["contributionCount"]) if days else None
    weekday = [0] * 7
    for d in days:
        weekday[d["weekday"]] += d["contributionCount"]
    langs = {}
    for repo in (user.get("repositories") or {}).get("nodes") or []:
        for e in ((repo or {}).get("languages") or {}).get("edges") or []:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    repos = []
    for item in cc.get("commitContributionsByRepository") or []:
        rep = item.get("repository") or {}
        repos.append(("private repository" if rep.get("isPrivate") else rep.get("name", "?"),
                      item["contributions"]["totalCount"]))
    return dict(
        weeks=[[(d["date"], d["contributionCount"], LEVELS.get(d["contributionLevel"], 0)) for d in w["contributionDays"]]
               for w in cc["contributionCalendar"]["weeks"]],
        total=cc["contributionCalendar"]["totalContributions"],
        active=sum(1 for c in counts if c), longest=longest, current=cur,
        busiest=(busiest["date"], busiest["contributionCount"]) if busiest and busiest["contributionCount"] else None,
        weekday=weekday, langs=sorted(langs.items(), key=lambda kv: -kv[1]), repos=repos,
        mix=[("Commits", cc["totalCommitContributions"]), ("Pull requests", cc["totalPullRequestContributions"]),
             ("Issues", cc["totalIssueContributions"]), ("Reviews", cc["totalPullRequestReviewContributions"])],
        synced=dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y, %H:%M UTC"),
    )


def empty():
    today = dt.date.today()
    start = today - dt.timedelta(days=today.weekday() + 1 + 52 * 7)
    weeks = [[((start + dt.timedelta(days=w * 7 + d)).isoformat(), 0, 0) for d in range(7)] for w in range(53)]
    return dict(weeks=weeks, total=None, active=None, longest=None, current=None, busiest=None,
                weekday=[0] * 7, langs=[], repos=[], mix=[], synced=None)


def fmt(n):
    return "—" if n is None else f"{n:,}"


# ── drawing ─────────────────────────────────────────────────────────────────
def panel(s, x, y, w, h, label, note=""):
    t = s.t
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["surface"]}" stroke="{t["line"]}"/>'
          f'<rect x="{x+22}" y="{y}" width="28" height="3" fill="{t["accent"]}"/>')
    s.text(x + 22, y + 32, label, "mono", 11.5, 500, fill="accent", ls=0.8)
    if note:
        s.text(x + w - 22, y + 32, note, "mono", 11, 400, fill="faint", anchor="end")


def board(data, theme):
    W = 1200
    s = Svg(W, 760, "Insights: a year of GitHub activity for SahajIVVIX-1, with contribution heatmap, "
                    "weekly rhythm, language mix and where commits landed", theme)
    t = dict(s.t, **EXTRA[theme]); s.t = t
    s.css.append(".up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}"
                 "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
                 ".col{opacity:0;animation:col .5s ease-out forwards}@keyframes col{to{opacity:1}}"
                 ".grow{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);"
                 "animation:grow 1.1s cubic-bezier(.2,.7,.2,1) forwards}@keyframes grow{to{transform:scaleX(1)}}"
                 ".rise{transform-box:fill-box;transform-origin:center bottom;transform:scaleY(0);"
                 "animation:rise .9s cubic-bezier(.2,.7,.2,1) forwards}@keyframes rise{to{transform:scaleY(1)}}"
                 ".ring{animation:ring 1.4s cubic-bezier(.2,.7,.2,1) forwards}"
                 ".hot{animation:hot 2.4s ease-in-out infinite}@keyframes hot{50%{opacity:.25}}")
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="759" rx="18" fill="{t["bg"]}" stroke="{t["line"]}"/>')

    # ── KPI row ──
    kpis = [("CONTRIBUTIONS", fmt(data["total"]), "last 12 months"),
            ("ACTIVE DAYS", fmt(data["active"]), "of the last 365"),
            ("LONGEST STREAK", fmt(data["longest"]), "days in a row"),
            ("CURRENT STREAK", fmt(data["current"]), "days and counting"),
            ("BUSIEST DAY", fmt(data["busiest"][1]) if data["busiest"] else "—",
             dt.date.fromisoformat(data["busiest"][0]).strftime("%a %d %b %Y") if data["busiest"] else "awaiting first sync")]
    kw = (W - 64 - 4 * 12) / 5
    for i, (lab, val, sub) in enumerate(kpis):
        x = 32 + i * (kw + 12)
        s.add(f'<g class="up" style="animation-delay:{0.1 + i*0.1:.2f}s">')
        s.add(f'<rect x="{x:.1f}" y="32" width="{kw:.1f}" height="108" rx="14" fill="{t["surface"]}" stroke="{t["line"]}"/>')
        s.text(x + 20, 60, lab, "mono", 11, 500, fill="faint", ls=0.8)
        s.text(x + 18, 106, val, "serif", 40, 400, fill="accent" if i == 0 else "text", ls=-1, extra=DIGITS + "—")
        s.text(x + 20, 127, sub, "mono", 11, 400, fill="muted")
        s.add("</g>")

    # ── heatmap ──
    hx, hy = 32, 156
    panel(s, hx, hy, 856, 236, "CONTRIBUTION FIELD", "one cell per day  ·  darker = busier")
    cell, gap = 12, 3
    gx, gy = hx + 54, hy + 62
    shades = [t["surface2"]] + [t["accent"]] * 4
    alpha = [1, 0.28, 0.5, 0.75, 1]
    for i, d in enumerate([1, 3, 5]):
        s.text(gx - 12, gy + d * (cell + gap) + 10, WEEKDAYS[d], "mono", 10.5, 400, fill="faint", anchor="end")
    last_month = None
    hot = data["busiest"][0] if data["busiest"] else None
    for wi, week in enumerate(data["weeks"]):
        x = gx + wi * (cell + gap)
        first = dt.date.fromisoformat(week[0][0])
        if first.month != last_month and first.day <= 7 and wi < len(data["weeks"]) - 1:
            s.text(x, gy - 10, first.strftime("%b"), "mono", 10.5, 400, fill="faint")
            last_month = first.month
        s.add(f'<g class="col" style="animation-delay:{0.3 + wi*0.025:.3f}s">')
        for date, n, lvl in week:
            wd = (dt.date.fromisoformat(date).weekday() + 1) % 7
            y = gy + wd * (cell + gap)
            cls = ' class="hot"' if date == hot else ""
            s.add(f'<rect{cls} x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{shades[lvl]}" '
                  f'fill-opacity="{alpha[lvl]}"/>')
        s.add("</g>")
    # sweeping scan line
    span = len(data["weeks"]) * (cell + gap)
    s.add(f'<rect class="scan" x="{gx-2}" y="{gy-4}" width="3" height="{7*(cell+gap)+5}" rx="1.5" fill="{t["accent"]}" opacity=".55"/>')
    s.css.append(f".scan{{animation:scan 9s linear 2s infinite;opacity:0}}"
                 f"@keyframes scan{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:.6}}94%{{opacity:.6}}"
                 f"100%{{transform:translateX({span}px);opacity:0}}}}")
    # legend
    ly = gy + 7 * (cell + gap) + 26
    s.text(gx, ly, "less", "mono", 10.5, 400, fill="faint")
    for i in range(5):
        s.add(f'<rect x="{gx + 34 + i*16}" y="{ly-10}" width="12" height="12" rx="3" fill="{shades[i]}" fill-opacity="{alpha[i]}"/>')
    s.text(gx + 34 + 5 * 16 + 4, ly, "more", "mono", 10.5, 400, fill="faint")
    if hot:
        s.add(f'<rect x="{gx + 200}" y="{ly-10}" width="12" height="12" rx="3" fill="{t["accent"]}"/>')
        s.text(gx + 218, ly, "pulsing cell = busiest day", "mono", 10.5, 400, fill="faint")

    # ── weekly rhythm ──
    rx, ry, rw = 900, 156, 268
    panel(s, rx, ry, rw, 236, "WEEKLY RHYTHM")
    wk = data["weekday"]
    top = max(wk) or 1
    peak = wk.index(max(wk)) if any(wk) else None
    bw, bgap, base, bh = 24, 10, ry + 196, 120
    bx0 = rx + (rw - (7 * bw + 6 * bgap)) / 2
    for i in range(7):
        x = bx0 + i * (bw + bgap)
        h = max(4, bh * wk[i] / top) if any(wk) else 4
        col = t["accent"] if i == peak else t["blue"]
        s.add(f'<rect x="{x:.1f}" y="{base-bh}" width="{bw}" height="{bh}" rx="5" fill="{t["surface2"]}"/>')
        s.add(f'<rect class="rise" style="animation-delay:{0.6 + i*0.08:.2f}s" x="{x:.1f}" y="{base-h:.1f}" '
              f'width="{bw}" height="{h:.1f}" rx="5" fill="{col}"/>')
        s.text(x + bw / 2, base + 18, WEEKDAYS[i][0], "mono", 11, 500 if i == peak else 400,
               fill="accent" if i == peak else "faint", anchor="middle")
    s.text(rx + rw - 22, ry + 32, f"peak: {WEEKDAYS[peak]}" if peak is not None else "", "mono", 11, 400,
           fill="faint", anchor="end")

    # ── language mix ──
    lx, ly0, lw, lh = 32, 408, 376, 320
    panel(s, lx, ly0, lw, lh, "LANGUAGE MIX", "public repos, by bytes")
    palette = [t["accent"], t["blue"], t["olive"], t["gold"], t["plum"], t["muted"]]
    langs = data["langs"]
    tot = sum(v for _, v in langs) or 1
    shown = langs[:5] + ([("Other", sum(v for _, v in langs[5:]))] if len(langs) > 5 else [])
    bx, by, bwid = lx + 22, ly0 + 56, lw - 44
    s.add(f'<rect x="{bx}" y="{by}" width="{bwid}" height="14" rx="7" fill="{t["surface2"]}"/>')
    s.add(f'<clipPath id="lbar"><rect x="{bx}" y="{by}" width="{bwid}" height="14" rx="7"/></clipPath>'
          f'<g clip-path="url(#lbar)"><g class="grow" style="animation-delay:.6s">')
    x = bx
    for i, (name, v) in enumerate(shown):
        w = bwid * v / tot
        s.add(f'<rect x="{x:.1f}" y="{by}" width="{w+0.5:.1f}" height="14" fill="{palette[i]}"/>')
        x += w
    s.add("</g></g>")
    y = by + 50
    for i, (name, v) in enumerate(shown):
        s.add(f'<g class="up" style="animation-delay:{0.8 + i*0.08:.2f}s">')
        s.add(f'<rect x="{bx}" y="{y-10}" width="10" height="10" rx="2.5" fill="{palette[i]}"/>')
        s.text(bx + 20, y, name, "sans", 15, 400, fill="text")
        s.text(bx + bwid, y, f"{100*v/tot:.1f}%", "mono", 13, 500, fill="muted", anchor="end")
        s.add(f'<line x1="{bx}" y1="{y+14}" x2="{bx+bwid}" y2="{y+14}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        s.add("</g>")
        y += 38
    if not shown:
        s.text(bx, y, "awaiting first sync", "mono", 12, 400, fill="faint")

    # ── where commits landed ──
    cx0, cw = 420, 420
    panel(s, cx0, ly0, cw, lh, "WHERE COMMITS LANDED", "top repos, last 12 months")
    repos = data["repos"][:6]
    topc = max([c for _, c in repos] or [1])
    y = ly0 + 66
    for i, (name, c) in enumerate(repos):
        s.add(f'<g class="up" style="animation-delay:{0.7 + i*0.08:.2f}s">')
        s.text(cx0 + 22, y, f"{i+1:02d}", "mono", 11, 500, fill="faint")
        nm = name
        while measure(nm, "sans", 400, 14.5) > cw - 150 and len(nm) > 4:
            nm = nm[:-2] + "…" if not nm.endswith("…") else nm[:-2] + "…"
        s.text(cx0 + 50, y, nm, "sans", 14.5, 400, fill="text")
        s.text(cx0 + cw - 22, y, fmt(c), "mono", 13, 500, fill="accent" if i == 0 else "muted", anchor="end")
        s.add("</g>")
        bwid = cw - 72
        s.add(f'<rect x="{cx0+50}" y="{y+9}" width="{bwid}" height="4" rx="2" fill="{t["surface2"]}"/>'
              f'<rect class="grow" style="animation-delay:{0.9 + i*0.08:.2f}s" x="{cx0+50}" y="{y+9}" '
              f'width="{max(4, bwid*c/topc):.1f}" height="4" rx="2" fill="{t["accent"] if i == 0 else t["blue"]}"/>')
        y += 42
    if not repos:
        s.text(cx0 + 22, y, "awaiting first sync", "mono", 12, 400, fill="faint")

    # ── contribution mix (donut) ──
    mx0, mw = 852, 316
    panel(s, mx0, ly0, mw, lh, "CONTRIBUTION MIX")
    mix = data["mix"]
    mt = sum(v for _, v in mix)
    ccx, ccy, r = mx0 + mw / 2, ly0 + 140, 62
    s.add(f'<circle cx="{ccx}" cy="{ccy}" r="{r}" fill="none" stroke="{t["surface2"]}" stroke-width="16"/>')
    mcol = [t["accent"], t["blue"], t["olive"], t["gold"]]
    off = 0
    for i, (name, v) in enumerate(mix):
        if not mt or not v:
            continue
        frac = 100 * v / mt
        seg = max(frac - 0.6, 0.4)
        s.add(f'<circle class="ring" style="animation-name:ring{i};animation-delay:{0.8 + i*0.15:.2f}s" cx="{ccx}" cy="{ccy}" '
              f'r="{r}" fill="none" stroke="{mcol[i]}" stroke-width="16" pathLength="100" stroke-dasharray="0 100" '
              f'transform="rotate({-90 + off*3.6:.2f} {ccx} {ccy})"/>')
        s.css.append(f"@keyframes ring{i}{{to{{stroke-dasharray:{seg:.2f} 100}}}}")
        off += frac
    s.text(ccx, ccy + 6, fmt(mt) if mt else "—", "serif", 30, 400, fill="text", anchor="middle", extra=DIGITS + "—")
    s.text(ccx, ccy + 26, "past year", "mono", 10.5, 400, fill="faint", anchor="middle")
    y = ly0 + 244
    for i, (name, v) in enumerate(mix):
        col, row = i % 2, i // 2
        x = mx0 + 22 + col * 142
        yy = y + row * 34
        s.add(f'<rect x="{x}" y="{yy-10}" width="10" height="10" rx="2.5" fill="{mcol[i]}"/>')
        s.text(x + 18, yy, name, "sans", 13.5, 400, fill="muted")
        s.text(x + 18 + measure(name, "sans", 400, 13.5) + 8, yy, fmt(v), "mono", 12.5, 500, fill="text", extra=DIGITS)
    if not mix:
        s.text(mx0 + 22, y, "awaiting first sync", "mono", 12, 400, fill="faint")

    return s, data["synced"]


def main():
    login = os.environ.get("USER_NAME", "SahajIVVIX-1")
    token = os.environ.get("ACCESS_TOKEN")
    data = empty()
    if token:
        try:
            data = digest(fetch(login, token))
        except Exception as e:  # keep the last good board rather than failing the run
            print(f"insights: fetch failed, leaving existing SVGs untouched ({e})")
            return
    elif os.environ.get("INSIGHTS_SAMPLE"):
        with open(os.environ["INSIGHTS_SAMPLE"]) as fh:
            data = digest(json.load(fh))
    for theme in THEMES:
        svg, _ = board(data, theme)
        path = os.path.join(OUT, f"insights-{theme}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg.render())
        print(f"{os.path.getsize(path)/1024:6.1f} KB  insights-{theme}.svg")


if __name__ == "__main__":
    main()
