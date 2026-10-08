"""A tiny mascot that travels through the whole README, one image at a time.

GitHub renders each SVG as a separate <img>, so there is no shared canvas. The
trick: every SVG on the route carries the *same* looping timeline (same
duration, same keyframe times), expressed in its own coordinates. When one image
shows the mascot leaving its bottom edge, the image below shows it arriving.

Route coordinates are "README units": the content column is 1200 wide, and y
runs down the page from the top of the hero. LAYOUT was measured from the README
rendered at GitHub's 830px column width (scale 1200/830); gaps between images
(buttons, prose, the recognition table) are where the mascot is off-stage.

Only CSS keyframes are used, so it plays inside GitHub's image proxy, and under
prefers-reduced-motion the mascot stays hidden.
"""
import math
import random
from layout import toolkit_layout

SCALE = 1200 / 830
_PX = {  # name: (x, y, w, h) in px at an 830px column, top of hero = y 53
    "hero": (35, 53, 830, 325), "impact": (35, 426, 830, 104),
    "section-about": (35, 564, 830, 58), "section-experience": (35, 812, 830, 58),
    "experience": (35, 886, 830, 268), "section-work": (35, 1204, 830, 58),
    "rag-pipeline": (35, 1278, 830, 530), "card-openenv": (35, 1824, 407, 281),
    "card-dcgan": (35, 2126, 407, 281), "card-microplastic": (35, 2427, 830, 104),
    "section-toolkit": (35, 2633, 830, 58), "toolkit": (35, 2707, 830, 433),
    "section-recognition": (35, 3190, 830, 58), "section-signals": (35, 3714, 830, 58),
    "telemetry": (35, 3788, 830, 353), "insights": (35, 4157, 830, 526),
    "footer": (35, 4733, 830, 173),
}
VIEW = {"card-openenv": (584, 404), "card-dcgan": (584, 404)}  # others are 1200 wide
# section rule lines: (start x, end x) at local y 48, from build.section()
BRIDGE = {"section-about": (170, 1129), "section-experience": (255, 1020), "section-work": (303, 1067),
          "section-toolkit": (190, 1051), "section-recognition": (270, 926), "section-signals": (185, 1012)}

SPEED = 200.0  # README units per second while walking
T_TURN = 0.18


def rect(name):
    x, y, w, h = _PX[name]
    return (x - 35) * SCALE, (y - 53) * SCALE, w * SCALE, h * SCALE


def scale_of(name):
    vw = VIEW.get(name, (1200,))[0]
    return vw / rect(name)[2]


def g(name, lx, ly):
    """local SVG coords -> README units"""
    ox, oy, _, _ = rect(name)
    k = scale_of(name)
    return ox + lx / k, oy + ly / k


# normals: which way the mascot's head points (it stands on the surface)
UP, DOWN, LEFT, RIGHT = 0, 180, -90, 90
B = 6  # inset so the feet sit on a border drawn at 0.5 / W-0.5


# ── walking on type: the top edge of every glyph ───────────────────────────
import os as _os
from fontTools.ttLib import TTFont as _TTFont
from fontTools.pens.boundsPen import BoundsPen as _BoundsPen

_FONTS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fonts")
_FILES = {("sans", 400, "normal"): "hanken-grotesk-latin-400-normal.woff2",
          ("sans", 600, "normal"): "hanken-grotesk-latin-600-normal.woff2",
          ("serif", 400, "normal"): "newsreader-latin-400-normal.woff2",
          ("serif", 400, "italic"): "newsreader-latin-400-italic.woff2"}
_fcache = {}


def _font(key):
    if key not in _fcache:
        f = _TTFont(_os.path.join(_FONTS, _FILES[key]))
        _fcache[key] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _fcache[key]


def advance(text, role="sans", weight=400, size=16, style="normal"):
    """same metric as build.measure()"""
    f, _, cmap, upm = _font((role, weight, style))
    return sum(f["hmtx"][cmap[ord(c)]][0] if ord(c) in cmap else upm * 0.5 for c in text) * size / upm


def glyph_tops(runs, role, size, x0, baseline, ls=0.0):
    """runs: [(text, weight, style)] laid out from x0. Returns [(x_left, x_right, y_top)] per inked glyph."""
    out, x = [], x0
    for text, wgt, st in runs:
        f, gs, cmap, upm = _font((role, wgt, st))
        k = size / upm
        for ch in text:
            gname = cmap.get(ord(ch))
            adv = f["hmtx"][gname][0] if gname else upm * 0.5
            if gname and not ch.isspace():
                pen = _BoundsPen(gs)
                gs[gname].draw(pen)
                if pen.bounds:
                    xmin, _, xmax, ymax = pen.bounds
                    out.append((x + xmin * k, x + xmax * k, baseline - ymax * k))
            x += adv * k + ls
    return out


def route():
    """[(kind, (x, y), normal)] in README units. kind: walk | hop | leap | fall.
    Besides borders and rules, the crew runs across the tops of letters (names,
    titles, tagline), the impact numbers and the insights tiles."""
    r = []
    def add(kind, name, lx, ly, n):
        r.append((kind, g(name, lx, ly), n))

    def letters(name, tops, reverse=False, first="leap", step="hop"):
        seq = list(reversed(tops)) if reverse else tops
        # merge neighbouring glyphs of similar height into one stretch, so the
        # walk follows the word shape without a keyframe per letter
        merged = []
        for xa, xb, top in seq:
            if merged:
                pa, pb, pt = merged[-1]
                gap = (xa - pb) if not reverse else (pa - xb)
                if gap < 9 and abs(top - pt) < 7:
                    merged[-1] = (min(pa, xa), max(pb, xb), min(pt, top))
                    continue
            merged.append((xa, xb, top))
        seq = merged
        prev = None
        for i, (xa, xb, top) in enumerate(seq):
            a_, b_ = (xb - 1.5, xa + 1.5) if reverse else (xa + 1.5, xb - 1.5)
            if i == 0:
                kind = first
            else:
                gap = abs(a_ - prev[0])
                kind = "walk" if gap < 4 and abs(top - prev[1]) < 2.5 else step if gap < 150 else "leap"
            add(kind, name, a_, top, UP)
            if abs(b_ - a_) > 1:
                add("walk", name, b_, top, UP)
            prev = (b_, top)

    def title(sec, text):  # section titles: serif 40 at x 40, baseline 58
        return glyph_tops([(text, 400, "normal")], "serif", 40, 40, 58, -0.5)

    # ── hero: down the left border, then over the name and the tagline ──
    add("start", "hero", 0.5, 30, RIGHT)
    add("walk", "hero", 0.5, 112, RIGHT)
    letters("hero", glyph_tops([("Sahaj ", 400, "normal"), ("Saliya", 400, "italic")], "serif", 96, 68, 196, -2))
    letters("hero", glyph_tops([("AI Engineer & Researcher building agents that", 400, "normal")], "sans", 25, 72, 248), reverse=True)
    letters("hero", glyph_tops([("retrieve, reason and learn.", 400, "normal")], "sans", 25, 72, 282))
    add("leap", "hero", 460, 469.5, UP)
    add("walk", "hero", 1170, 469.5, UP)
    # ── impact: drop onto the numbers and skip across them right to left ──
    nums = ["0.81", "1.00", "37%", "2"]
    for i in reversed(range(4)):
        tops = glyph_tops([(nums[i], 400, "normal")], "serif", 52, i * 300 + 34, 78, -1)
        letters("impact", tops, reverse=True, first="fall" if i == 3 else "leap")
    # ── About: over the title, then along the rule ──
    letters("section-about", title("section-about", "About"))
    add("hop", "section-about", 170 + 26, 48, UP)
    add("walk", "section-about", 1129 - 30, 48, UP)
    # drop behind the About paragraph onto the Experience rule, then over its title
    add("fall", "section-experience", 1020 - 30, 48, UP)
    add("walk", "section-experience", 255 + 26, 48, UP)
    letters("section-experience", title("section-experience", "Experience"), reverse=True, first="hop")
    # flip under the timeline rail and hang from it all the way across (the rail sits
    # 16px from the image top, too close to stand on without the antenna being cut),
    # then swing onto the right card. -180 is "upside down", turning the short way to LEFT.
    add("leap", "experience", 22, 15, -180)
    add("walk", "experience", 1186, 15, -180)
    add("leap", "experience", 1199.5, 96, LEFT)
    add("walk", "experience", 1199.5, 372, LEFT)
    # ── Selected work: rule, title, then the RAG headline and subtitle ──
    add("leap", "section-work", 1067 - 40, 48, UP)
    add("walk", "section-work", 303 + 26, 48, UP)
    letters("section-work", title("section-work", "Selected work"), reverse=True, first="hop")
    letters("rag-pipeline", glyph_tops([("Enterprise Agentic RAG Orchestrator", 600, "normal")], "sans", 34, 40, 104, -0.6))
    letters("rag-pipeline", glyph_tops([("Production-grade multi-agent RAG with a self-correcting retrieval loop.", 400, "italic")],
                                       "serif", 20, 40, 138), reverse=True)
    add("leap", "rag-pipeline", 0.5, 170, RIGHT)
    add("walk", "card-microplastic", 0.5, 132, RIGHT)
    # ── Toolkit: over the title, along the rule, down the right edge ──
    letters("section-toolkit", title("section-toolkit", "Toolkit"))
    add("hop", "section-toolkit", 190 + 26, 48, UP)
    add("walk", "section-toolkit", 1051 - 30, 48, UP)
    # then zig-zag through every category: chip tops, the category name, the
    # divider below, picking a different way through each row
    rnd = random.Random(11)
    rows, _ = toolkit_layout(lambda it: advance(it, "sans", 400, 15.5))
    cx, first = 1021, "fall"
    for ri, (label, _, line, top, bottom) in enumerate(rows):
        # chips on the row's first line (wrapped lines sit too close below it)
        chips = [(x + 9, x + w - 9, top - 0.5) for x, y, w, _ in line if y == top]
        if ri:  # skip a few chips at random; row 1 has no headroom for the jump arc
            kept, skipped = [], False
            for i, c in enumerate(chips):  # never two in a row, so a skip stays a short hop
                skipped = not skipped and 0 < i < len(chips) - 1 and rnd.random() < 0.3
                if not skipped:
                    kept.append(c)
            chips = kept
        name = [gt for gt in glyph_tops([(label, 400, "normal")], "serif", 27, 52, (top + bottom) / 2 - 4, -0.3)
                if gt[2] > 27]  # letters too close to the image top would cut off the antenna
        step = "hop" if ri else "walk"
        if cx > 600:   # coming from the right: chips first, then the name
            letters("toolkit", chips, reverse=True, first=first, step=step)
            if name:
                letters("toolkit", name, reverse=True, first="hop")
            cx = 60
        else:
            if name:
                letters("toolkit", name, first=first)
            letters("toolkit", chips, first="hop", step=step)
            cx = chips[-1][1]
        if ri + 1 < len(rows):
            dy = rows[ri + 1][3] - 28
            add("fall", "toolkit", cx, dy - 0.5, UP)
            # stroll a little along the divider, or run right across it
            nxt = rows[ri + 1][2]
            far = max(x + w for x, y, w, _ in nxt if y == nxt[0][1]) - 12
            cx = (far if cx < 600 else 50) if rnd.random() < 0.5 else max(30, min(far, cx + rnd.choice((-1, 1)) * rnd.uniform(60, 200)))
            add("walk", "toolkit", cx, dy - 0.5, UP)
            first = "hop"
    # ── Recognition rule and title, drop behind the table onto the Signals title and rule ──
    add("leap", "section-recognition", 926 - 30, 48, UP)
    add("walk", "section-recognition", 270 + 26, 48, UP)
    letters("section-recognition", title("section-recognition", "Recognition"), reverse=True, first="hop")
    letters("section-signals", title("section-signals", "Signals"), first="fall")
    add("hop", "section-signals", 185 + 26, 48, UP)
    add("walk", "section-signals", 1012 - 30, 48, UP)
    # ── telemetry console's right border, then the insights tiles and panels ──
    add("leap", "telemetry", 1199.5, 70, LEFT)
    add("walk", "insights", 1199.5, 14, LEFT)
    kw = (1200 - 64 - 4 * 12) / 5
    tiles = [(32 + i * (kw + 12) + 14, 32 + i * (kw + 12) + kw - 14, 32.5) for i in range(5)]
    letters("insights", tiles, reverse=True, first="hop")
    add("leap", "insights", 46, 156.5, UP)
    add("walk", "insights", 874, 156.5, UP)
    add("hop", "insights", 914, 156.5, UP)
    add("walk", "insights", 1154, 156.5, UP)
    add("hop", "insights", 1199.5, 190, LEFT)
    add("walk", "footer", 1199.5, 232, LEFT)
    add("walk", "footer", 1182, 249.5, UP)
    add("walk", "footer", 30, 249.5, UP)
    return r


def _image_at(x, y):
    for name in _PX:
        ox, oy, w, h = rect(name)
        if ox - 0.5 <= x <= ox + w + 0.5 and oy - 0.5 <= y <= oy + h + 0.5:
            return name


def frames():
    """Expand the route into timed samples: [(t, x, y, angle, flip)]."""
    pts = route()
    out, t = [], 0.6
    (_, (x, y), n) = pts[0]
    flip = 1
    out.append((t, x, y, n, flip))
    for kind, (nx, ny), nn in pts[1:]:
        dx, dy = nx - x, ny - y
        dist = math.hypot(dx, dy)
        # facing: the mascot's local +x after rotating by the surface normal
        a = math.radians(n if kind == "walk" else 0)
        lx = dx * math.cos(a) + dy * math.sin(a)
        nf = 1 if lx >= 0 else -1
        if nf != flip:
            t += T_TURN
            out.append((t, x, y, n, nf))
            flip = nf
        if kind == "walk":
            dur = dist / SPEED
            # rotate around corners over a short stretch, otherwise keep the normal
            if nn != n:
                out.append((t + dur * 0.5, x + dx * 0.5, y + dy * 0.5, (n + nn) / 2 if abs(nn - n) <= 180 else n, flip))
            t += dur
            out.append((t, nx, ny, nn, flip))
        else:
            if kind == "hop":  # a quick skip from one letter or tile to the next
                kind, hop, dur = "leap", 7 + min(dist, 40) / 6, 0.2 + dist / 700
            else:
                hop = 26 if kind == "leap" else 10
                dur = 0.55 + dist / 900 if kind == "leap" else 0.4 + math.sqrt(max(dy, 1)) / 26
            # keep the arc inside the picture: a jump within one image never lifts the antenna past its top
            box = _image_at(x, y)
            if box and box == _image_at(nx, ny) and n == 0 and nn == 0:
                k = scale_of(box)
                room = (min(y, ny) - rect(box)[1]) * k - 27
                hop = max(1.5, min(hop, room / k)) if room < hop * k else hop
            beat = 0.12 if dur > 0.4 else 0.03
            out.append((t + beat, x, y, n, flip))  # crouch beat before the jump
            t += beat
            steps = 10
            for i in range(1, steps + 1):
                u = i / steps
                ease = u if kind == "leap" else u * u
                px = x + dx * (u if kind == "leap" else math.sin(u * math.pi / 2))
                py = y + dy * ease - hop * 4 * u * (1 - u)
                ang = n + (nn - n) * u
                out.append((t + dur * u, px, py, ang, 1 if dx >= 0 else -1))
            flip = 1 if dx >= 0 else -1
            t += dur
            out.append((t + beat, nx, ny, nn, flip))  # landing beat
            t += beat
        x, y, n = nx, ny, nn
    return out, t + 0.6


def _densify(fr, step=120.0):
    """split long straight runs so every image they pass through gets keyframes"""
    out = [fr[0]]
    for a, b in zip(fr, fr[1:]):
        n = int(math.hypot(b[1] - a[1], b[2] - a[2]) // step)
        for i in range(1, n + 1):
            u = i / (n + 1)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u,
                        a[3] + (b[3] - a[3]) * u, a[4]))
        out.append(b)
    return out


FRAMES, _END = frames()
FRAMES = _densify(FRAMES)
_T0 = FRAMES[0][0]
D = _END - _T0          # one full traversal of the route, in seconds
_TAUS = [f[0] - _T0 for f in FRAMES]

# ── the crew ────────────────────────────────────────────────────────────────
# Five mascots share the route. Each one walks it like a ghost bouncing between
# the two ends; where two ghosts would pass through each other, the mascots
# bounce off instead (identical speeds make that the same set of positions with
# the labels swapped). So mascot k is simply the k-th ghost in route order: it
# roams back and forth between its neighbours, collides head-on, turns around,
# and the whole dance repeats exactly every 2*D seconds with no reset.
CREW = ["accent", "blue", "olive", "gold", "plum"]
N = len(CREW)
P = 2 * D
EXTRA = {"#141413": dict(gold="#D4B06A", plum="#B48EAD"), "#FAF9F5": dict(gold="#8C6A1F", plum="#7A4F74")}


def at(tau):
    """route position at route-time tau: (x, y, angle)"""
    tau = min(max(tau, 0.0), D)
    lo, hi = 0, len(_TAUS) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _TAUS[mid] <= tau:
            lo = mid
        else:
            hi = mid
    a, b = FRAMES[lo], FRAMES[hi]
    span = _TAUS[hi] - _TAUS[lo]
    u = 0.0 if span <= 1e-9 else (tau - _TAUS[lo]) / span
    return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, a[3] + (b[3] - a[3]) * u


def _ghost(j, t):
    u = (t / P + j / N + 0.037 * j) % 1.0
    return 2 * D * u if u < 0.5 else 2 * D * (1 - u)


def simulate(dt=0.01):
    steps = int(P / dt)
    order_prev, prev = None, None
    pieces = [[] for _ in range(N)]   # per mascot: [(t, tau)] breakpoints
    hits = []                         # (t, tau, k) mascots k and k+1 collide
    slope_prev = [None] * N
    for i in range(steps + 1):
        t = i * dt
        gs = sorted(_ghost(j, t) for j in range(N))
        order = sorted(range(N), key=lambda j: _ghost(j, t))
        if prev is not None:
            for k in range(N):
                s = 1 if gs[k] > prev[k] else -1
                if s != slope_prev[k]:
                    pieces[k].append((t - dt, prev[k]))
                    slope_prev[k] = s
            if order != order_prev:
                for k in range(N - 1):
                    if order[k] != order_prev[k]:
                        hits.append((t, (gs[k] + gs[k + 1]) / 2, k))
                        break
        prev, order_prev = gs, order
    for k in range(N):
        pieces[k].append((P, _ghost_sorted(k, P)))
    return pieces, hits


def _ghost_sorted(k, t):
    return sorted(_ghost(j, t) for j in range(N))[k]


def track(points):
    """Expand a mascot's (t, tau) breakpoints into (t, x, y, angle, face) keyframes."""
    out = []
    for (ta, ua), (tb, ub) in zip(points, points[1:]):
        s = 1 if ub >= ua else -1
        inner = [u for u in _TAUS if min(ua, ub) < u < max(ua, ub)]
        if s < 0:
            inner.reverse()
        for u in [ua] + inner:
            out.append([ta + abs(u - ua), *at(u)])
    out.append([points[-1][0], *at(points[-1][1])])
    # facing from motion, in the mascot's own frame; hold it through pauses
    face = 1
    for i, f in enumerate(out):
        nxt = out[i + 1] if i + 1 < len(out) else None
        if nxt:
            vx, vy = nxt[1] - f[1], nxt[2] - f[2]
            a = math.radians(f[3])
            lx = vx * math.cos(a) + vy * math.sin(a)
            if abs(lx) > 0.5:
                face = 1 if lx > 0 else -1
        f.append(face)
    return out


PIECES, HITS = simulate()
TRACKS = [track(p) for p in PIECES]


def _pct(t):
    return f"{100 * t / P:.3f}".rstrip("0").rstrip(".") + "%"


def attach(s, name):
    """Add the crew (and their collisions) to Svg `s`, an image named `name`."""
    if name not in _PX:
        return
    t = dict(s.t, **EXTRA.get(s.t["bg"], {}))
    ox, oy, w, h = rect(name)
    k = scale_of(name)
    m = 70
    near = lambda x, y: ox - m <= x <= ox + w + m and oy - m <= y <= oy + h + m
    loc = lambda x, y: ((x - ox) * k, (y - oy) * k)
    css = [".mjb{animation:mjb .36s ease-in-out infinite alternate}@keyframes mjb{to{transform:translateY(-1.6px)}}"
           ".mjl{transform-box:fill-box;transform-origin:top center;animation:mjl .36s ease-in-out infinite alternate}"
           ".mjl2{animation-direction:alternate-reverse}@keyframes mjl{from{transform:rotate(-24deg)}to{transform:rotate(24deg)}}"
           ".mjk{animation:mjk 4.2s infinite}@keyframes mjk{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.1)}}"
           ".mja{animation:mja 1.6s ease-in-out infinite}@keyframes mja{50%{opacity:.35}}"
           ".bst{opacity:0}"]
    body = []
    for c, tr in enumerate(TRACKS):
        flags = [near(f[1], f[2]) for f in tr]
        if not any(flags):
            continue
        keep = [i for i in range(len(tr)) if flags[i] or (i and flags[i - 1]) or (i + 1 < len(tr) and flags[i + 1])]
        mv, vis, eye = [], [], []
        last_p = None
        for i in keep:
            tt, x, y, ang, _ = tr[i]
            p = _pct(tt)
            if p == last_p:
                continue
            last_p = p
            lx, ly = loc(x, y)
            rot = f" rotate({ang:.0f}deg)" if round(ang) else ""
            mv.append(f"{p}{{transform:translate({lx:.0f}px,{ly:.0f}px){rot}}}")
        # visibility: hidden while the mascot is far from this image
        shown = None
        for i, f in enumerate(tr):
            v = flags[i] or (i and flags[i - 1]) or (i + 1 < len(tr) and flags[i + 1])
            if v != shown:
                tt = f[0] if v else tr[i - 1][0]
                vis.append(f"{_pct(tt)}{{opacity:{1 if v else 0}}}")
                vis.append(f"{100 * tt / P + 0.001:.3f}%{{opacity:{1 if v else 0}}}")
                shown = v
        # the eye glides across the face when the mascot turns around: no mirroring
        cur = tr[0][4]
        eye.append(f"0%{{transform:translateX({2.6 * cur:.1f}px)}}")
        for f in tr[1:]:
            if f[4] != cur:
                eye.append(f"{_pct(f[0])}{{transform:translateX({2.6 * cur:.1f}px)}}")
                eye.append(f"{_pct(min(f[0] + 0.32, P))}{{transform:translateX({2.6 * f[4]:.1f}px)}}")
                cur = f[4]
        eye.append(f"100%{{transform:translateX({2.6 * cur:.1f}px)}}")
        css.append(f"@keyframes mv{c}{{{''.join(mv)}}}@keyframes vs{c}{{0%{{opacity:0}}{''.join(vis)}}}"
                   f"@keyframes ey{c}{{{''.join(eye)}}}"
                   f".mv{c}{{animation:mv{c} {P:.2f}s linear infinite}}.vs{c}{{opacity:0;animation:vs{c} {P:.2f}s step-end infinite}}"
                   f".ey{c}{{animation:ey{c} {P:.2f}s ease-in-out infinite}}")
        col = t[CREW[c]]
        body.append(
            f'<g class="vs{c}"><g class="mv{c}"><g class="mjb" style="animation-delay:-{0.07 * c:.2f}s">'
            f'<line class="mjl" x1="-3" y1="-6" x2="-3" y2="0" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<line class="mjl mjl2" x1="3" y1="-6" x2="3" y2="0" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<rect x="-7.5" y="-17" width="15" height="12" rx="5" fill="{col}"/>'
            f'<g class="ey{c}"><g class="mjk" style="transform-box:fill-box;transform-origin:center">'
            f'<circle cx="0" cy="-11.6" r="2.4" fill="{t["bg"]}"/></g></g>'
            f'<line x1="0" y1="-17" x2="0" y2="-21.5" stroke="{col}" stroke-width="1.4" stroke-linecap="round"/>'
            f'<circle class="mja" cx="0" cy="-22.6" r="1.7" fill="{col}"/></g></g></g>')
    # collisions: the two mascots bounce apart and a two-colour spark ring bursts where they met
    for n, (tc, tau, kk) in enumerate(HITS):
        x, y, ang = at(tau)
        if not (ox - 10 <= x <= ox + w + 10 and oy - 10 <= y <= oy + h + 10):
            continue
        lx, ly = loc(x, y)
        c1, c2 = t[CREW[kk]], t[CREW[kk + 1]]
        a0, a1, a2 = _pct(max(tc - 0.02, 0)), _pct(tc + 0.05), _pct(min(tc + 0.9, P))
        css.append(f"@keyframes bs{n}{{0%,{a0}{{opacity:0;transform:scale(.2) rotate(0deg)}}"
                   f"{a1}{{opacity:1;transform:scale(.6) rotate(10deg)}}{a2}{{opacity:0;transform:scale(1.7) rotate(70deg)}}"
                   f"100%{{opacity:0;transform:scale(.2)}}}}")
        sparks = "".join(
            f'<circle cx="{14 * math.cos(i * math.pi / 5):.1f}" cy="{14 * math.sin(i * math.pi / 5):.1f}" r="{2.2 if i % 2 else 1.6}" '
            f'fill="{c1 if i % 2 else c2}"/>' for i in range(10))
        ra = math.radians(ang)
        body.append(f'<g transform="translate({lx + 11 * math.sin(ra):.1f} {ly - 11 * math.cos(ra):.1f}) rotate({ang:.0f})"><g class="bst" '
                    f'style="animation:bs{n} {P:.2f}s linear infinite">'
                    f'<circle r="9" fill="none" stroke="{c1}" stroke-width="1.4"/>'
                    f'<circle r="5" fill="none" stroke="{c2}" stroke-width="1.2" stroke-dasharray="2 3"/>{sparks}</g></g>')
    if body:
        s.css.append("".join(css))
        s.add("".join(body))
