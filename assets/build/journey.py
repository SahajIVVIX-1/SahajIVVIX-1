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

SPEED = 175.0  # README units per second while walking
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


def route():
    """[(kind, (x, y), normal)] in README units. kind: walk | leap | fall."""
    r = []
    def add(kind, name, lx, ly, n):
        r.append((kind, g(name, lx, ly), n))
    # hero: start at the top-left, crawl down the left border, along the bottom, out at the bottom-right
    add("start", "hero", 0.5, 30, RIGHT)
    add("walk", "hero", 0.5, 452, RIGHT)
    add("walk", "hero", 18, 469.5, UP)
    add("walk", "hero", 1170, 469.5, UP)
    # drop off the bottom-right corner past the buttons, onto the impact strip's right border
    add("fall", "impact", 1199.5, 22, LEFT)
    add("walk", "impact", 1199.5, 132, LEFT)
    # leap onto the About rule, cross it right to left
    add("leap", "section-about", 1129 - 30, 48, UP)
    add("walk", "section-about", 170 + 26, 48, UP)
    # drop behind the About paragraph and land on the Experience rule
    add("fall", "section-experience", 255 + 30, 48, UP)
    add("walk", "section-experience", 1020 - 30, 48, UP)
    # hop onto the timeline rail, run to its end, then crawl down the right card
    add("leap", "experience", 1110, 16, UP)
    add("walk", "experience", 1186, 16, UP)
    add("leap", "experience", 1199.5, 96, LEFT)
    add("walk", "experience", 1199.5, 372, LEFT)
    # leap onto the Selected work rule, cross it to the left
    add("leap", "section-work", 1067 - 40, 48, UP)
    add("walk", "section-work", 303 + 30, 48, UP)
    # jump down onto the RAG card's left border and crawl all the way down the left column
    add("leap", "rag-pipeline", 0.5, 46, RIGHT)
    add("walk", "card-microplastic", 0.5, 132, RIGHT)
    # leap over the Toolkit title onto its rule, cross it to the right
    add("leap", "section-toolkit", 190 + 50, 48, UP)
    add("walk", "section-toolkit", 1051 - 30, 48, UP)
    # drop onto the toolkit's first row rule, run to the edge, crawl down it
    add("leap", "toolkit", 1150, 92, UP)
    add("walk", "toolkit", 1184, 92, UP)
    add("walk", "toolkit", 1199.5, 108, LEFT)
    add("walk", "toolkit", 1199.5, 610, LEFT)
    # Recognition rule right to left, then drop behind the table onto the Signals rule
    add("leap", "section-recognition", 926 - 30, 48, UP)
    add("walk", "section-recognition", 270 + 30, 48, UP)
    add("fall", "section-signals", 185 + 30, 48, UP)
    add("walk", "section-signals", 1012 - 30, 48, UP)
    # down the right border of the telemetry console, the insights board and the footer
    add("leap", "telemetry", 1199.5, 70, LEFT)
    add("walk", "footer", 1199.5, 232, LEFT)
    add("walk", "footer", 1182, 249.5, UP)
    add("walk", "footer", 30, 249.5, UP)
    return r


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
            hop = 26 if kind == "leap" else 10
            dur = 0.55 + dist / 900 if kind == "leap" else 0.4 + math.sqrt(max(dy, 1)) / 26
            out.append((t + 0.12, x, y, n, flip))  # crouch beat before the jump
            t += 0.12
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
            out.append((t + 0.1, nx, ny, nn, flip))  # landing beat
            t += 0.1
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
    return f"{100 * t / P:.3f}%"


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
            mv.append(f"{p}{{transform:translate({lx:.1f}px,{ly:.1f}px) rotate({ang:.1f}deg)}}")
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
