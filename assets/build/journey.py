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


FRAMES, PERIOD = frames()


def attach(s, name):
    """Add the mascot to Svg `s` (an image named `name` in LAYOUT)."""
    if name not in _PX:
        return
    t = s.t
    ox, oy, _, _ = rect(name)
    k = scale_of(name)
    kf, last = [], None
    for tt, x, y, ang, flip in FRAMES:
        p = f"{100 * tt / PERIOD:.3f}%"
        if p == last:
            continue
        last = p
        lx, ly = (x - ox) * k, (y - oy) * k
        kf.append(f"{p}{{transform:translate({lx:.1f}px,{ly:.1f}px) rotate({ang:.1f}deg) scaleX({flip})}}")
    t0, t1 = FRAMES[0], FRAMES[-1]
    kf.insert(0, f"0%{{transform:translate({(t0[1]-ox)*k:.1f}px,{(t0[2]-oy)*k:.1f}px) rotate({t0[3]}deg)}}")
    kf.append(f"100%{{transform:translate({(t1[1]-ox)*k:.1f}px,{(t1[2]-oy)*k:.1f}px) rotate({t1[3]}deg) scaleX({t1[4]})}}")
    fade = f"{100 * 0.5 / PERIOD:.3f}%"
    s.css.append(
        f"@keyframes mjr{{{''.join(kf)}}}"
        f".mj{{animation:mjr {PERIOD:.2f}s linear infinite}}"
        f".mjw{{opacity:0;animation:mjw {PERIOD:.2f}s linear infinite}}"
        f"@keyframes mjw{{0%{{opacity:0}}{fade}{{opacity:1}}{100 - float(fade[:-1]):.3f}%{{opacity:1}}100%{{opacity:0}}}}"
        ".mjb{animation:mjb .36s ease-in-out infinite alternate}@keyframes mjb{to{transform:translateY(-1.6px)}}"
        ".mjl{transform-box:fill-box;transform-origin:top center;animation:mjl .36s ease-in-out infinite alternate}"
        ".mjl2{animation-direction:alternate-reverse}@keyframes mjl{from{transform:rotate(-24deg)}to{transform:rotate(24deg)}}"
        ".mje{animation:mje 4.2s infinite}@keyframes mje{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.1)}}"
        ".mja{animation:mja 1.6s ease-in-out infinite}@keyframes mja{50%{opacity:.35}}")
    a, bg = t["accent"], t["bg"]
    # feet at (0,0), head toward -y. ~20 units tall, no backing shape of any kind.
    s.add(f'<g class="mjw"><g class="mj"><g class="mjb">'
          f'<line class="mjl" x1="-3" y1="-6" x2="-3" y2="0" stroke="{a}" stroke-width="2.2" stroke-linecap="round"/>'
          f'<line class="mjl mjl2" x1="3" y1="-6" x2="3" y2="0" stroke="{a}" stroke-width="2.2" stroke-linecap="round"/>'
          f'<rect x="-7.5" y="-17" width="15" height="12" rx="5" fill="{a}"/>'
          f'<g class="mje" style="transform-box:fill-box;transform-origin:center">'
          f'<circle cx="2.6" cy="-11.6" r="2.4" fill="{bg}"/></g>'
          f'<line x1="-1.5" y1="-17" x2="-3.5" y2="-21.5" stroke="{a}" stroke-width="1.4" stroke-linecap="round"/>'
          f'<circle class="mja" cx="-3.8" cy="-22.4" r="1.7" fill="{a}"/>'
          f'</g></g></g>')
