"""Generate the profile README's animated SVGs (dark + light).

Every SVG embeds subsetted copies of three OFL fonts, so the typography
survives GitHub's image proxy (GitHub strips CSS and web fonts from Markdown).

    pip install fonttools brotli pillow
    python assets/build/build.py          # run from the repo root

Edit CONTENT below, re-run, commit the regenerated files in assets/.
"""
import base64, html, io, os, re
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # assets/
FONTS = os.path.join(HERE, "fonts")
PORTRAIT = os.environ.get("PORTRAIT", os.path.join(OUT, "..", "Sahaj.png"))

# ── design tokens ───────────────────────────────────────────────────────────
THEMES = {
    "dark": dict(bg="#141413", surface="#1C1B18", surface2="#24231F", line="#35332D",
                 text="#F5F4EE", muted="#A8A598", faint="#6E6C63", accent="#D97757",
                 blue="#7FA8D4", olive="#9DB17A", grid="#2A2925"),
    "light": dict(bg="#FAF9F5", surface="#F3F1EA", surface2="#ECE9DF", line="#DCD7CA",
                  text="#1A1915", muted="#5C5A52", faint="#8F8C80", accent="#BD5A37",
                  blue="#3B6A98", olive="#56693A", grid="#E9E5DA"),
}
FONT_FILES = {
    ("sans", 400, "normal"): "hanken-grotesk-latin-400-normal.woff2",
    ("sans", 600, "normal"): "hanken-grotesk-latin-600-normal.woff2",
    ("serif", 400, "normal"): "newsreader-latin-400-normal.woff2",
    ("serif", 400, "italic"): "newsreader-latin-400-italic.woff2",
    ("mono", 400, "normal"): "jetbrains-mono-latin-400-normal.woff2",
    ("mono", 500, "normal"): "jetbrains-mono-latin-500-normal.woff2",
}
FAMILY = {"sans": "HG", "serif": "NR", "mono": "JB"}
_tt = {k: TTFont(os.path.join(FONTS, v)) for k, v in FONT_FILES.items()}


def measure(s, role="sans", weight=400, size=16, style="normal"):
    f = _tt[(role, weight, style)]
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    w = 0
    for ch in s:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g else upm * 0.5
    return w * size / upm


def esc(s):
    return html.escape(s, quote=True)


# ── tiny SVG builder ────────────────────────────────────────────────────────
class Svg:
    def __init__(self, w, h, title, theme):
        self.w, self.h, self.title, self.t = w, h, title, THEMES[theme]
        self.body, self.css, self.chars = [], [], {k: set() for k in FONT_FILES}

    def text(self, x, y, s, role="sans", size=16, weight=400, style="normal",
             fill="text", anchor="start", cls="", ls=0, raw=None):
        """raw: list of (string, weight, fill, style) runs for mixed styling."""
        runs = raw or [(s, weight, fill, style)]
        parts = []
        for r, wgt, fl, st in runs:
            self.chars[(role, wgt, st)].update(r)
            parts.append(f'<tspan font-weight="{wgt}" font-style="{st}" fill="{self.t.get(fl, fl)}">{esc(r)}</tspan>')
        a = f' class="{cls}"' if cls else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        self.body.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[role]}" font-size="{size}" '
                         f'text-anchor="{anchor}"{l}{a}>{"".join(parts)}</text>')

    def add(self, s):
        self.body.append(s)

    def c(self, key):
        return self.t[key]

    def render(self):
        faces = []
        for (role, wgt, st), chars in self.chars.items():
            if not chars:
                continue
            opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]
            font = TTFont(os.path.join(FONTS, FONT_FILES[(role, wgt, st)]))
            sub = subset.Subsetter(opts); sub.populate(text="".join(chars) + " "); sub.subset(font)
            buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            faces.append(f"@font-face{{font-family:{FAMILY[role]};font-weight:{wgt};font-style:{st};"
                         f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
        css = "\n".join(faces + self.css + [
            "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"])
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{esc(self.title)}"><title>{esc(self.title)}</title>'
                f"<style>{css}</style>{''.join(self.body)}</svg>")


def save(name, build):
    for theme in THEMES:
        svg = build(theme)
        path = os.path.join(OUT, f"{name}-{theme}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg.render())
        print(f"{os.path.getsize(path)/1024:6.1f} KB  {os.path.relpath(path, OUT)}")


def wrap(runs, role, size, maxw):
    """runs: text with **bold** marks. Returns lines as lists of (word, bold)."""
    words = []
    for i, part in enumerate(re.split(r"\*\*", runs)):
        for w in part.split():
            words.append((w, i % 2 == 1))
    lines, cur, curw = [], [], 0
    space = measure(" ", role, 400, size)
    for w, b in words:
        ww = measure(w, role, 600 if b else 400, size)
        if cur and curw + space + ww > maxw:
            lines.append(cur); cur, curw = [], 0
        curw += (space if cur else 0) + ww
        cur.append((w, b))
    if cur:
        lines.append(cur)
    return lines


def line_runs(words, base="muted", strong="text"):
    out = []
    for i, (w, b) in enumerate(words):
        s = ("" if i == 0 else " ") + w
        if out and out[-1][1] == (600 if b else 400):
            out[-1] = (out[-1][0] + s,) + out[-1][1:]
        else:
            out.append((s, 600 if b else 400, strong if b else base, "normal"))
    return out


def arrow(x, y, size, color, kind="ne"):
    """Draw ↗ or → as a path (the fonts' Latin subsets have no arrows)."""
    s = size
    if kind == "ne":
        d = f"M{x} {y+s} L{x+s} {y} M{x+s*0.35} {y} L{x+s} {y} L{x+s} {y+s*0.65}"
    else:
        d = f"M{x} {y} L{x+s} {y} M{x+s*0.6} {y-s*0.4} L{x+s} {y} L{x+s*0.6} {y+s*0.4}"
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def grid_bg(s, w, h, fade=True):
    t = s.t
    s.add(f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
          f'<circle cx="1.5" cy="1.5" r="1.1" fill="{t["grid"]}"/></pattern>'
          f'<radialGradient id="fade" cx="70%" cy="40%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity="1"/>'
          f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
          f'<mask id="m"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask></defs>'
          f'<rect width="{w}" height="{h}" rx="18" fill="{t["bg"]}"/>'
          f'<rect width="{w}" height="{h}" rx="18" fill="url(#dots)" mask="url(#m)"/>')


# ── 1. hero ─────────────────────────────────────────────────────────────────
def portrait_b64():
    im = Image.open(PORTRAIT).convert("L")
    w, h = im.size
    ch = int(w / 0.8)
    im = im.crop((0, 0, w, min(h, ch))).resize((440, 550), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


PORTRAIT_B64 = portrait_b64() if os.path.exists(PORTRAIT) else None
FOCUS = ["Large Language Models", "Agentic AI", "Retrieval-Augmented Generation", "Reinforcement Learning"]


def hero(theme):
    W, H = 1200, 470
    s = Svg(W, H, "Sahaj Saliya, AI Engineer and Researcher: LLMs, Agentic AI, RAG, Reinforcement Learning", theme)
    t = s.t
    grid_bg(s, W, H)
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["line"]}"/>')
    # drifting glow
    s.add(f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.22"/>'
          f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient></defs>'
          f'<circle class="glow" cx="930" cy="230" r="300" fill="url(#glow)"/>')
    s.css.append(".glow{animation:drift 14s ease-in-out infinite alternate;transform-origin:930px 230px}"
                 "@keyframes drift{0%{transform:translate(-40px,10px) scale(.9)}100%{transform:translate(30px,-20px) scale(1.1)}}")
    s.css.append(".up{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}"
                 "@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
                 ".d1{animation-delay:.1s}.d2{animation-delay:.35s}.d3{animation-delay:.6s}.d4{animation-delay:.85s}.d5{animation-delay:1.1s}")
    x = 72
    # status pill
    s.add(f'<g class="up d1"><rect x="{x}" y="62" width="356" height="32" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>'
          f'<circle cx="{x+20}" cy="78" r="5" fill="{t["olive"]}"/><circle class="ping" cx="{x+20}" cy="78" r="5" fill="none" stroke="{t["olive"]}"/>')
    s.text(x + 36, 83, "OPEN TO AI ENGINEERING & RESEARCH ROLES", "mono", 12.5, 500, fill="muted", ls=0.6)
    s.add("</g>")
    s.css.append(".ping{animation:ping 2s ease-out infinite;transform-origin:92px 78px}"
                 "@keyframes ping{0%{transform:scale(1);opacity:.9}100%{transform:scale(3);opacity:0}}")
    # name
    s.add('<g class="up d2">')
    s.text(x - 4, 196, "", "serif", 96, raw=[("Sahaj ", 400, "text", "normal"), ("Saliya", 400, "accent", "italic")], ls=-2)
    s.add("</g>")
    s.add('<g class="up d3">')
    s.text(x, 248, "AI Engineer & Researcher building agents that", "sans", 25, 400, fill="text")
    s.text(x, 282, "retrieve, reason and learn.", "sans", 25, 400, fill="text")
    s.add("</g>")
    # rotating focus line
    s.add('<g class="up d4">')
    s.text(x, 338, "focus", "mono", 15, 400, fill="faint")
    fx = x + measure("focus", "mono", 400, 15) + 14
    s.add(arrow(fx, 333, 14, t["accent"], "e"))
    n = len(FOCUS); per = 2.6; total = n * per
    for i, word in enumerate(FOCUS):
        s.add(f'<g class="rot" style="animation-delay:{i*per}s">')
        s.text(fx + 26, 338, word, "mono", 15, 500, fill="accent")
        s.add("</g>")
    a0, a1, a2 = 100 * 0.06 / n, 100 * 0.9 / n, 100 * 1.0 / n
    s.css.append(f".rot{{opacity:0;animation:rot {total}s infinite}}"
                 f"@keyframes rot{{0%{{opacity:0;transform:translateY(8px)}}{a0:.2f}%{{opacity:1;transform:none}}"
                 f"{a1:.2f}%{{opacity:1;transform:none}}{a2:.2f}%{{opacity:0;transform:translateY(-8px)}}100%{{opacity:0}}}}")
    s.add("</g>")
    # meta row
    s.add('<g class="up d5">')
    s.add(f'<line x1="{x}" y1="376" x2="{x+620}" y2="376" stroke="{t["line"]}"/>')
    meta = [("B.Tech ICT", "PDEU · CGPA 8.5 · 2027"), ("Based in", "Gandhinagar, India"), ("Last role", "R&D Intern · HNNOIX")]
    mx = x
    for k, v in meta:
        s.text(mx, 404, k.upper(), "mono", 11, 400, fill="faint", ls=0.8)
        s.text(mx, 428, v, "sans", 15.5, 600, fill="text")
        mx += 228
    s.add("</g>")
    # portrait card
    px, py, pw, ph = 860, 58, 264, 330
    s.add(f'<g class="up d3"><g transform="rotate(2.2 {px+pw/2} {py+ph/2})">'
          f'<rect x="{px-10}" y="{py-10}" width="{pw+20}" height="{ph+56}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>'
          f'<clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10"/></clipPath>')
    if PORTRAIT_B64:
        s.add(f'<image x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice" '
              f'clip-path="url(#pc)" href="data:image/jpeg;base64,{PORTRAIT_B64}"/>')
    s.add(f'<defs><linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
          f'<stop offset=".85" stop-color="{t["accent"]}" stop-opacity=".18"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity=".55"/></linearGradient></defs>'
          f'<g clip-path="url(#pc)"><rect class="scan" x="{px}" y="{py-90}" width="{pw}" height="90" fill="url(#scan)"/></g>')
    s.css.append(f".scan{{animation:scan 4.5s cubic-bezier(.6,0,.4,1) infinite}}"
                 f"@keyframes scan{{0%{{transform:translateY(0)}}70%,100%{{transform:translateY({ph+90}px)}}}}")
    s.text(px + 4, py + ph + 32, "fig. 1", "serif", 17, 400, style="italic", fill="text")
    s.text(px + pw - 2, py + ph + 32, "the engineer, rendered in ASCII", "mono", 10.5, 400, fill="faint", anchor="end")
    s.add("</g></g>")
    return s


# ── 2. section headers ──────────────────────────────────────────────────────
SECTIONS = [
    ("about", "01", "About", "whoami"),
    ("experience", "02", "Experience", "where I have shipped"),
    ("work", "03", "Selected work", "flagship first"),
    ("toolkit", "04", "Toolkit", "what I reach for"),
    ("recognition", "05", "Recognition", "papers, hackathons, certificates"),
    ("signals", "06", "Signals", "live GitHub activity"),
]


def section(num, title, caption):
    def build(theme):
        W, H = 1200, 84
        s = Svg(W, H, f"{num}. {title}", theme)
        t = s.t
        s.text(0, 56, num, "mono", 15, 500, fill="accent")
        s.text(40, 58, title, "serif", 40, 400, fill="text", ls=-0.5)
        tx = 40 + measure(title, "serif", 400, 40) + 24
        cw = measure(caption, "mono", 400, 13)
        s.add(f'<line class="draw" x1="{tx}" y1="48" x2="{W - cw - 24}" y2="48" stroke="{t["line"]}" stroke-width="1.2" '
              f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        s.add(f'<circle class="dot" cx="{tx}" cy="48" r="3.5" fill="{t["accent"]}"/>')
        s.text(W, 52, caption, "mono", 13, 400, fill="faint", anchor="end")
        s.css.append(".draw{animation:draw 1.6s cubic-bezier(.6,0,.2,1) .2s forwards}@keyframes draw{to{stroke-dashoffset:0}}"
                     f".dot{{animation:slide 1.6s cubic-bezier(.6,0,.2,1) .2s forwards}}"
                     f"@keyframes slide{{to{{transform:translateX({W - cw - 24 - tx}px)}}}}")
        return s
    return build


# ── 3. impact strip ─────────────────────────────────────────────────────────
STATS = [
    ("0.81", "RAGAS faithfulness", "Multi-Agent RAG orchestrator"),
    ("1.00", "context precision", "same system, RAGAS eval"),
    ("37%", "fewer false-positive signals", "agentic trading systems"),
    ("2", "papers presented", "IEEE AIMV 2025"),
]


def stats(theme):
    W, H = 1200, 150
    s = Svg(W, H, "Impact: RAGAS faithfulness 0.81, context precision 1.00, 37% fewer false-positive signals, 2 IEEE AIMV 2025 papers", theme)
    t = s.t
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>')
    cw = W / len(STATS)
    for i, (num, label, sub) in enumerate(STATS):
        x = i * cw + 34
        if i:
            s.add(f'<line x1="{i*cw}" y1="28" x2="{i*cw}" y2="{H-28}" stroke="{t["line"]}"/>')
        s.add(f'<g class="up" style="animation-delay:{0.15 + i*0.18:.2f}s">')
        s.text(x, 78, num, "serif", 52, 400, fill="text", ls=-1)
        s.text(x, 104, label, "sans", 15.5, 600, fill="text")
        s.text(x, 124, sub, "mono", 11.5, 400, fill="faint")
        s.add("</g>")
        s.add(f'<rect class="bar" style="animation-delay:{0.5 + i*0.18:.2f}s" x="{x}" y="{H-3}" width="{cw-68}" height="3" rx="1.5" fill="{t["accent"]}"/>')
    s.css.append(".up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}"
                 "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
                 ".bar{transform:scaleX(0);transform-box:fill-box;animation:grow 1s cubic-bezier(.6,0,.2,1) forwards}"
                 "@keyframes grow{to{transform:scaleX(1)}}")
    return s


# ── 4. experience timeline ──────────────────────────────────────────────────
EXPERIENCE = [
    ("May – Jul 2026", "Research & Innovation Intern", "HNNOIX Private Limited", [
        "Built reusable AI infrastructure for **6G R&D:** an LLM Gateway, RAG Runtime, AI Memory Layer and Knowledge Base.",
        "Enabled scalable agent execution, context management and workflow orchestration.",
        "Applied GenAI, RAG and agent-based decision-making to network architectures and communication systems.",
    ]),
    ("Dec 2024 – Jun 2025", "Freelance Financial AI Engineer", "Quantitative Investment Analysis", [
        "Shipped **2 autonomous trading-signal systems** using Agentic AI and RAG over live market news.",
        "**Cut false-positive signals by 37%** with confidence scoring and filtering rules.",
        "Built a **CrewAI** research pipeline over GPT-4, Bloomberg, FMP and Alpha Vantage for automated earnings analysis.",
    ]),
]


def experience(theme):
    W = 1200
    colw, gap, pad = 572, 56, 30
    lines = [[wrap(b, "sans", 16, colw - pad * 2 - 22) for b in e[3]] for e in EXPERIENCE]
    body_h = max(sum(len(l) * 25 + 12 for l in ls) for ls in lines)
    H = 76 + 112 + body_h + 14
    s = Svg(W, H, "Experience: Research & Innovation Intern at HNNOIX (May to Jul 2026); Freelance Financial AI Engineer (Dec 2024 to Jun 2025)", theme)
    t = s.t
    # rail
    s.add(f'<line x1="14" y1="16" x2="{W-14}" y2="16" stroke="{t["line"]}" stroke-width="1.2"/>'
          f'<line class="rail" x1="14" y1="16" x2="{W-14}" y2="16" stroke="{t["accent"]}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
    s.css.append(".rail{animation:draw 2.2s cubic-bezier(.6,0,.2,1) .2s forwards}@keyframes draw{to{stroke-dashoffset:0}}"
                 ".up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}"
                 "@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}")
    for i, (dates, role, org, _) in enumerate(EXPERIENCE):
        x = i * (colw + gap)
        s.add(f'<circle cx="{x+30}" cy="16" r="7" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>'
              f'<circle cx="{x+30}" cy="16" r="3" fill="{t["accent"]}"/>'
              f'<line x1="{x+30}" y1="23" x2="{x+30}" y2="66" stroke="{t["accent"]}" stroke-width="1.2" stroke-dasharray="2 4"/>')
        s.text(x + 44, 48, dates.upper(), "mono", 12.5, 500, fill="accent", ls=0.6)
        s.add(f'<g class="up" style="animation-delay:{0.4 + i*0.5}s">')
        s.add(f'<rect x="{x+0.5}" y="66.5" width="{colw-1}" height="{H-67}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>')
        s.text(x + pad, 110, role, "sans", 23, 600, fill="text")
        s.text(x + pad, 140, org, "serif", 19, 400, style="italic", fill="muted")
        y = 188
        for bl in lines[i]:
            s.add(f'<rect x="{x+pad}" y="{y-11}" width="8" height="2" fill="{t["accent"]}"/>')
            for ln in bl:
                s.text(x + pad + 22, y, "", "sans", 16, raw=line_runs(ln))
                y += 25
            y += 12
        s.add("</g>")
    return s


# ── 5. flagship pipeline ────────────────────────────────────────────────────
def pipeline(theme):
    W, H = 1200, 490
    s = Svg(W, H, "Enterprise Agentic RAG Orchestrator architecture: guard, semantic cache, supervisor, CRAG / NL-to-SQL / human-in-the-loop workers, validator", theme)
    t = s.t
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="{t["surface"]}" stroke="{t["line"]}"/>')
    nodes = {
        "q": (40, 168, 118, "Query", "user"),
        "g": (190, 168, 150, "Injection guard", "security"),
        "c": (372, 168, 150, "Semantic cache", "Qdrant ANN"),
        "s": (556, 168, 140, "Supervisor", "router"),
        "w1": (742, 82, 170, "Corrective RAG", "worker"),
        "w2": (742, 168, 170, "NL-to-SQL", "worker"),
        "w3": (742, 254, 170, "Human-in-loop", "email tool"),
        "v": (946, 168, 120, "Validator", "agent"),
        "a": (1094, 168, 76, "Answer", ""),
    }
    NH = 56

    def mid(k, side):
        x, y, w, *_ = nodes[k]
        return (x + w, y + NH / 2) if side == "r" else (x, y + NH / 2)

    def curve(a, b):
        (x1, y1), (x2, y2) = mid(a, "r"), mid(b, "l")
        cx = (x1 + x2) / 2
        return f"M{x1} {y1} C{cx} {y1} {cx} {y2} {x2} {y2}"

    edges = [("q", "g"), ("g", "c"), ("c", "s"), ("s", "w1"), ("s", "w2"), ("s", "w3"),
             ("w1", "v"), ("w2", "v"), ("w3", "v"), ("v", "a")]
    paths = {}
    for a, b in edges:
        d = curve(a, b); paths[(a, b)] = d
        s.add(f'<path d="{d}" fill="none" stroke="{t["line"]}" stroke-width="1.6"/>')
    # cache-hit bypass
    cx1 = nodes["c"][0] + nodes["c"][2] / 2
    ax = nodes["a"][0] + nodes["a"][2] / 2
    hit = f"M{cx1} 168 C{cx1} 34 {ax} 34 {ax} 168"
    s.add(f'<path d="{hit}" fill="none" stroke="{t["olive"]}" stroke-width="1.4" stroke-dasharray="5 6" class="march"/>')
    s.add(f'<rect x="{(cx1+ax)/2-88}" y="52" width="176" height="24" rx="12" fill="{t["surface"]}" stroke="{t["line"]}"/>')
    s.text((cx1 + ax) / 2, 68.5, "cache hit · sub-ms", "mono", 11.5, 500, fill="olive", anchor="middle")
    s.css.append(".march{animation:march 1.2s linear infinite}@keyframes march{to{stroke-dashoffset:-22}}")
    # packets
    route = lambda *ks: " ".join(paths[(ks[i], ks[i + 1])] for i in range(len(ks) - 1))
    trips = [(("q", "g", "c", "s", "w1", "v", "a"), 0, "accent"), (("q", "g", "c", "s", "w2", "v", "a"), 2.1, "blue"),
             (("q", "g", "c", "s", "w3", "v", "a"), 4.2, "olive")]
    for ks, delay, col in trips:
        # each edge is its own subpath; join into one continuous path for animateMotion
        d = route(*ks)
        d = re.sub(r"\s+M[\d.]+ [\d.]+", "", d)  # consecutive edges share endpoints
        s.add(f'<circle r="5" fill="{t[col]}" opacity="0"><animateMotion dur="6.3s" begin="{delay}s" repeatCount="indefinite" path="{d}"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" dur="6.3s" begin="{delay}s" repeatCount="indefinite"/></circle>')
    for k, (x, y, w, label, sub) in nodes.items():
        hl = k in ("s", "w1")
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="12" fill="{t["bg"]}" '
              f'stroke="{t["accent"] if hl else t["line"]}" stroke-width="{1.6 if hl else 1.2}"/>')
        if sub:
            s.text(x + w / 2, y + 25, label, "sans", 15, 600, fill="text", anchor="middle")
            s.text(x + w / 2, y + 43, sub, "mono", 10.5, 400, fill="faint", anchor="middle")
        else:
            s.text(x + w / 2, y + 33, label, "sans", 15, 600, fill="accent", anchor="middle")
    # CRAG inner loop panel
    py = 340
    s.add(f'<rect x="40" y="{py}" width="1130" height="120" rx="14" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    s.text(62, py + 28, "INSIDE THE CORRECTIVE RAG WORKER", "mono", 11.5, 500, fill="accent", ls=0.8)
    steps = [("Hybrid retrieval", "Qdrant dense + BM25"), ("CrossEncoder rerank", "parent-child 200 / 800 tok"),
             ("LLM document grader", "relevant?"), ("Generate", "grounded answer")]
    sx = 62
    sw = 230
    for i, (a, b) in enumerate(steps):
        x = sx + i * (sw + 52)
        s.text(x, py + 58, a, "sans", 15, 600, fill="text")
        s.text(x, py + 78, b, "mono", 11, 400, fill="faint")
        if i < len(steps) - 1:
            s.add(arrow(x + sw + 6, py + 54, 26, t["muted"], "e"))
    # rewrite loop: grader back to retrieval
    gx = sx + 2 * (sw + 52) + 60
    s.add(f'<path class="march" d="M{gx} {py+86} C{gx} {py+106} {sx+60} {py+106} {sx+60} {py+86}" fill="none" '
          f'stroke="{t["accent"]}" stroke-width="1.4" stroke-dasharray="5 6"/>')
    s.add(f'<rect x="{(gx+sx+60)/2-86}" y="{py+91}" width="172" height="20" rx="10" fill="{t["bg"]}"/>')
    s.text((gx + sx + 60) / 2, py + 106, "irrelevant: rewrite query", "mono", 11, 500, fill="accent", anchor="middle")
    s.text(40, 34, "", "mono", 12, raw=[("RAGAS  ", 500, "faint", "normal"), ("faithfulness 0.81", 500, "text", "normal"),
                                        ("  ·  ", 400, "faint", "normal"), ("context precision 1.00", 500, "text", "normal")])
    return s


# ── 6. project cards ────────────────────────────────────────────────────────
PROJECTS = {
    "openenv": ("02", "Reinforcement learning", "OpenEnv", "RL data-cleaning agent",
                "An agent that learns how to clean data.", [
                    "Custom **Q-Learning environment;** a **Llama 3** agent picks cleaning actions from structured observations.",
                    "Reward shaping, anti-loop penalties and step limits that block destructive operations.",
                    "Pydantic-typed JSON outputs, FastAPI server, Docker on Hugging Face Spaces.",
                ], ["Q-Learning", "Llama 3", "FastAPI", "Docker", "HF Spaces"]),
    "xai": ("03", "Explainable ML · MLOps", "Student-Performance", "XAI platform",
            "End-to-end MLOps with explanations you can check.", [
                "Benchmarks **9 ML/DL models** (XGBoost, CatBoost, LightGBM, PyTorch, FLAML) with Pandera validation.",
                "**SHAP + LIME** attributions; Spearman rank correlation measures how far they agree.",
                "MLflow tracking, FastAPI + Streamlit, Docker Compose, GitHub Actions CI.",
            ], ["SHAP", "LIME", "MLflow", "Streamlit", "CI"]),
    "dcgan": ("04", "Generative models · research", "Modern DCGAN", "reproducibility study",
              "Re-implementing Radford et al. (2015), then upgrading it.", [
                  "Paper-faithful re-implementation, modernised with **LSGAN + Spectral Normalization.**",
                  "Custom GANAnalyzer hooks internal layers to visualise learned filters and feature maps.",
                  "Formal paper-vs-modern comparison and a 4-panel convergence dashboard.",
              ], ["PyTorch", "LSGAN", "SpectralNorm", "Research"]),
    "sentinel": ("05", "Systems · security", "SentinelProxy", "suite",
                 "Blocks malicious domains before a connection is made.", [
                     "Local Node.js **HTTPS proxy** and **DNS server** that drop malicious domains up front.",
                     "Millions of blocklist domains in indexed **SQLite3** for fast lookups.",
                     "Live Express + Socket.IO dashboard; automatic OS proxy/DNS hooks and firewall rules.",
                 ], ["Node.js", "SQLite3", "Socket.IO", "DNS"]),
}


def chips(s, x, y, items, maxx=None):
    t = s.t
    for it in items:
        w = measure(it, "mono", 400, 12) + 22
        s.add(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="none" stroke="{t["line"]}"/>')
        s.text(x + w / 2, y + 17.5, it, "mono", 12, 400, fill="muted", anchor="middle")
        x += w + 8
    return x


def card(key):
    num, kicker, title, title2, hook, bullets, tags = PROJECTS[key]

    def build(theme):
        W, pad = 584, 30
        wl = [wrap(b, "sans", 15, W - pad * 2 - 20) for b in bullets]
        H = 168 + sum(len(l) * 23 + 10 for l in wl) + 58
        H = max(H, 404)
        s = Svg(W, H, f"{title} {title2}: {hook}", theme)
        t = s.t
        s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>')
        s.add(f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
              f'<g clip-path="url(#cc)"><rect class="sweep" x="-160" y="0" width="160" height="3" fill="{t["accent"]}"/></g>')
        s.css.append(f".sweep{{animation:sweep 5s cubic-bezier(.6,0,.4,1) infinite}}@keyframes sweep{{0%{{transform:translateX(0)}}60%,100%{{transform:translateX({W+160}px)}}}}"
                     ".nudge{animation:nudge 2.4s ease-in-out infinite}@keyframes nudge{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}")
        s.text(pad, 46, "", "mono", 12, raw=[(num + "  ", 500, "accent", "normal"), (kicker.upper(), 400, "faint", "normal")], ls=0.6)
        s.add(f'<g class="nudge">{arrow(W-pad-16, 32, 16, t["muted"], "ne")}</g>')
        s.text(pad, 92, "", "sans", 28, raw=[(title + " ", 600, "text", "normal")], ls=-0.4)
        s.text(pad + measure(title + " ", "sans", 600, 28) - 0.4 * len(title), 92, title2, "serif", 26, 400, style="italic", fill="muted")
        s.text(pad, 124, hook, "serif", 18, 400, style="italic", fill="accent")
        y = 168
        for bl in wl:
            s.add(f'<rect x="{pad}" y="{y-10}" width="8" height="2" fill="{t["accent"]}"/>')
            for ln in bl:
                s.text(pad + 20, y, "", "sans", 15, raw=line_runs(ln))
                y += 23
            y += 10
        chips(s, pad, H - 50, tags)
        return s
    return build


def microplastic(theme):
    W, H, pad = 1200, 150, 30
    s = Svg(W, H, "Microplastic Detection (Smart India Hackathon): YOLOv11 fine-tuned for particle detection and size estimation", theme)
    t = s.t
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>')
    s.text(pad, 44, "", "mono", 12, raw=[("06  ", 500, "accent", "normal"), ("COMPUTER VISION · SMART INDIA HACKATHON", 400, "faint", "normal")], ls=0.6)
    s.text(pad, 86, "", "sans", 27, raw=[("Microplastic Detection", 600, "text", "normal")], ls=-0.4)
    s.text(pad, 116, "YOLOv11 (n/s/m/l) fine-tuned with custom hyperparameters for particle detection and size estimation.",
           "sans", 15, 400, fill="muted")
    chips(s, 880, 70, ["YOLOv11", "OpenCV", "CUDA"])
    s.add(f'<g class="nudge">{arrow(W-pad-16, 30, 16, t["muted"], "ne")}</g>')
    # animated detection boxes on the right edge
    s.css.append(".nudge{animation:nudge 2.4s ease-in-out infinite}@keyframes nudge{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}"
                 ".bx{opacity:0;animation:bx 3.6s infinite}@keyframes bx{0%,8%{opacity:0;transform:scale(1.3)}18%,70%{opacity:1;transform:scale(1)}80%,100%{opacity:0}}")
    for i, (bx, by, r) in enumerate([(905, 118, 4), (968, 112, 6), (1030, 122, 3.5), (1092, 114, 5)]):
        s.add(f'<circle cx="{bx}" cy="{by}" r="{r}" fill="{t["muted"]}"/>'
              f'<rect class="bx" style="animation-delay:{i*0.45}s;transform-origin:{bx}px {by}px" x="{bx-r-6}" y="{by-r-6}" '
              f'width="{2*r+12}" height="{2*r+12}" fill="none" stroke="{t["accent"]}" stroke-width="1.4" rx="2"/>')
    return s


# ── 7. toolkit ──────────────────────────────────────────────────────────────
TOOLKIT = [
    ("GenAI & agents", ["LangChain", "LangGraph", "CrewAI", "AWS Bedrock", "HF Transformers", "Pydantic", "RAGAS"]),
    ("ML · DL · RL", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "CatBoost", "LightGBM", "Q-Learning", "SHAP", "LIME"]),
    ("Retrieval & data", ["Qdrant", "ChromaDB", "PostgreSQL", "MongoDB", "Redis", "Hadoop", "SQL"]),
    ("Vision & OCR", ["OpenCV", "YOLOv11", "Kraken OCR", "ComfyUI"]),
    ("MLOps & infra", ["MLflow", "Docker", "Kubernetes", "FastAPI", "Flask", "Streamlit", "HF Spaces", "GitHub Actions", "AWS", "GCP", "Linux"]),
    ("Languages", ["Python", "C++", "SQL", "MATLAB"]),
]


def toolkit(theme):
    W, labw, rowh = 1200, 200, 0
    # lay out first to know height
    rows, y = [], 34
    for label, items in TOOLKIT:
        x, line = labw, []
        for it in items:
            w = measure(it, "sans", 400, 14.5) + 28
            if x + w > W - 24:
                y += 42; x = labw
            line.append((x, y, w, it)); x += w + 8
        rows.append((label, line, y)); y += 58
    H = y - 10
    s = Svg(W, H, "Toolkit: " + "; ".join(f"{l}: {', '.join(i)}" for l, i in TOOLKIT), theme)
    t = s.t
    s.css.append(".pop{opacity:0;animation:pop .5s cubic-bezier(.2,.7,.2,1) forwards}"
                 "@keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}")
    k = 0
    for ri, (label, line, ylast) in enumerate(rows):
        y0 = line[0][1]
        if ri:
            s.add(f'<line x1="0" y1="{y0-22}" x2="{W}" y2="{y0-22}" stroke="{t["line"]}"/>')
        s.text(0, y0 + 19, label.upper(), "mono", 12, 500, fill="accent" if ri == 0 else "faint", ls=0.6)
        for (x, y, w, it) in line:
            s.add(f'<g class="pop" style="animation-delay:{0.05 + k*0.035:.2f}s">'
                  f'<rect x="{x}" y="{y}" width="{w:.1f}" height="30" rx="8" fill="{t["surface"]}" stroke="{t["line"]}"/>')
            s.text(x + w / 2, y + 20, it, "sans", 14.5, 400, fill="text", anchor="middle")
            s.add("</g>"); k += 1
    return s


# ── 8. buttons + footer ─────────────────────────────────────────────────────
BUTTONS = ["Portfolio", "LinkedIn", "X", "Medium", "Résumé", "LeetCode"]


def button(label, primary=False):
    def build(theme):
        w = int(measure(label, "sans", 600, 15) + 66)
        s = Svg(w, 44, label, theme)
        t = s.t
        fill = t["text"] if primary else t["surface"]
        fg = t["bg"] if primary else t["text"]
        s.add(f'<rect x="0.5" y="0.5" width="{w-1}" height="43" rx="22" fill="{fill}" stroke="{t["text"] if primary else t["line"]}"/>')
        s.text(22, 27.5, label, "sans", 15, 600, fill=fg)
        s.add(arrow(w - 34, 16, 11, t["accent"], "ne"))
        return s
    return build


def footer(theme):
    W, H = 1200, 250
    s = Svg(W, H, "Open to AI Engineering & Research roles", theme)
    t = s.t
    grid_bg(s, W, H)
    s.add(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["line"]}"/>')
    # orbit motif
    cx, cy = 1010, 125
    for r, dur, col in [(46, 9, "accent"), (78, 15, "blue"), (108, 23, "olive")]:
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["line"]}"/>'
              f'<circle r="5" fill="{t[col]}"><animateMotion dur="{dur}s" repeatCount="indefinite" '
              f'path="M{cx+r} {cy} a{r} {r} 0 1 1 {-2*r} 0 a{r} {r} 0 1 1 {2*r} 0"/></circle>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{t["accent"]}"/>')
    s.text(72, 70, "WHAT'S NEXT", "mono", 12.5, 500, fill="accent", ls=0.8)
    s.text(70, 128, "Open to AI Engineering", "serif", 50, 400, fill="text", ls=-1)
    s.text(70, 180, "", "serif", 50, raw=[("& ", 400, "text", "normal"), ("Research", 400, "accent", "italic"), (" roles.", 400, "text", "normal")], ls=-1)
    s.text(72, 216, "Building open-source tools, publications and products around LLM agents.", "sans", 16, 400, fill="muted")
    return s


if __name__ == "__main__":
    save("hero", hero)
    save("impact", stats)
    for key, num, title, cap in SECTIONS:
        save(f"section-{key}", section(num, title, cap))
    save("experience", experience)
    save("rag-pipeline", pipeline)
    for k in PROJECTS:
        save(f"card-{k}", card(k))
    save("card-microplastic", microplastic)
    save("toolkit", toolkit)
    for i, b in enumerate(BUTTONS):
        slug = b.lower().replace("é", "e")
        save(f"btn-{slug}", button(b, primary=(i == 0)))
    save("footer", footer)
