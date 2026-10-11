"""Quantitative panels, monochrome.

Series identity never rests on colour here: the language meters are one series
per row with its own direct label, and the unit chart separates its two series
by fill (solid vs outline) plus a legend. Every figure traces to the portfolio
or the LinkedIn profile, and the unit chart sums to the same 10 projects and
9 recognitions the counters report.
"""

import math

from theme import (
    EDGE, INK, INK_DIM, INK_FAINT, INK_GHOST,
    base_css, corners, defs, prompt, shell, starfield, svg,
)

W = 1000


# --------------------------------------------------------------- counters --
def metrics(_root):
    uid = "m"
    h = 176
    tiles = [("10", "PROJECTS", "2024 – 2026"),
             ("09", "RECOGNITIONS", "awards &amp; grants"),
             ("07", "LANGUAGES", "in the core stack"),
             ("03", "ACTIVE ROLES", "held concurrently"),
             ("$9.5K", "GRANT", "Emergent Ventures"),
             ("01", "INCUBATION", "CIIC, NIT Jamshedpur")]
    pad, gap = 28, 10
    tw = (W - 2 * pad - gap * (len(tiles) - 1)) / len(tiles)
    out = []
    for i, (val, label, sub) in enumerate(tiles):
        x = pad + i * (tw + gap)
        mid = x + tw / 2
        size = 32 if len(val) <= 2 else 24
        out.append(f"""  <g class="pop" style="animation-delay:{0.2 + i * 0.09:.2f}s">
{corners(x, 62, tw, 88, 11, INK, 1.2, 0.5)}
    <text x="{mid:.1f}" y="106" text-anchor="middle" font-size="{size}"
          font-weight="bold" fill="{INK}" filter="url(#{uid}-glow)">{val}</text>
    <text x="{mid:.1f}" y="126" text-anchor="middle" font-size="9.5" fill="{INK}"
          letter-spacing="1.3">{label}</text>
    <text x="{mid:.1f}" y="140" text-anchor="middle" font-size="8.5"
          fill="{INK_FAINT}">{sub}</text>
  </g>""")
    body = f"""{defs(uid, 3.0)}
{shell(W, h)}
{starfield(W, h, 70, 2024, avoid=[(20, 56, 950, 100)])}
{prompt(W, "akshat --stats")}
{chr(10).join(out)}
"""
    return svg(W, h, body, base_css(), sw=("m", 12, 0.5))


# ------------------------------------------------------- language meters --
def meter(_root):
    """A dot-matrix meter per language: cells lit in proportion to share.
    One series per row, each directly labelled - no colour does any work."""
    uid = "l"
    langs = [("python", 27.4, "3.14"), ("typescript", 21.8, "5.9"),
             ("cpp", 14.6, "C++23"), ("rust", 11.9, "1.90"),
             ("javascript", 10.3, "ES2025"), ("onnx", 7.5, "opset 23"),
             ("ruby", 6.5, "3.4")]
    cells, cw, ch, gapx = 40, 10, 11, 3
    pitch = cw + gapx
    x0 = 158
    h = 80 + len(langs) * 34 + 52
    out = []
    for i, (name, pct, ver) in enumerate(langs):
        y = 96 + i * 34
        lit = max(1, round(pct / langs[0][1] * cells))
        lit_cells, dim_cells = [], []
        for c in range(cells):
            cx = x0 + c * pitch
            tgt = lit_cells if c < lit else dim_cells
            tgt.append(f'<rect x="{cx}" y="{y - 9}" width="{cw}" height="{ch}" '
                       f'fill="{INK if c < lit else INK_GHOST}"/>')
        row = (f'<g>{"".join(dim_cells)}</g>'
               f'<g class="fill" style="transform-origin:{x0}px {y}px;'
               f'animation-delay:{0.3 + i * 0.09:.2f}s">{"".join(lit_cells)}</g>')
        out.append(f"""  <g class="slide" style="animation-delay:{0.2 + i * 0.07:.2f}s">
    <text x="28" y="{y}" font-size="12.5" fill="{INK}">{name}</text>
    {row}
    <text x="{x0 + cells * pitch + 16}" y="{y}" font-size="12.5"
          font-weight="bold" fill="{INK}">{pct}%</text>
    <text x="{x0 + cells * pitch + 76}" y="{y}" font-size="10"
          fill="{INK_FAINT}">{ver}</text>
  </g>""")
    note = (f'  <text x="28" y="{h - 30}" font-size="10" fill="{INK_FAINT}">'
            f'Share of code across the 2024–2026 portfolio. One cell ≈ 0.7%; '
            f'the row scale tops out at the largest share.</text>'
            f'<text x="28" y="{h - 15}" font-size="10" fill="{INK_GHOST}">'
            f'toolchain: git · docker · linux · postgresql · aws · '
            f'raspberry pi · esp-idf · arduino · onnx runtime</text>')
    body = f"""{defs(uid)}
{shell(W, h)}
{starfield(W, h, 85, 1414, avoid=[(20, 62, 950, h - 110)])}
{prompt(W, "akshat/stack --by-share")}
{chr(10).join(out)}
{note}
"""
    return svg(W, h, body, base_css(), sw=("l", 16, 1.5))


# ------------------------------------------------------------ unit chart --
def units(_root):
    """One square per thing: solid = project shipped, outline = recognition."""
    uid = "u"
    w, h = 490, 316
    years = [("2024", 1, 1), ("2025", 4, 4), ("2026", 5, 4)]
    s, gap = 15, 6
    pitch = s + gap
    out = []
    for i, (yr, proj, rec) in enumerate(years):
        y = 104 + i * 54
        out.append(f'  <text x="28" y="{y + 12}" font-size="12.5" fill="{INK}">{yr}</text>')
        for j in range(proj):
            out.append(f'  <rect class="pop" style="animation-delay:{0.3 + i * 0.2 + j * 0.07:.2f}s" '
                       f'x="{84 + j * pitch}" y="{y}" width="{s}" height="{s}" fill="{INK}"/>')
        for j in range(rec):
            out.append(f'  <rect class="pop" style="animation-delay:{0.5 + i * 0.2 + j * 0.07:.2f}s" '
                       f'x="{300 + j * pitch}" y="{y}" width="{s}" height="{s}" fill="none" '
                       f'stroke="{INK}" stroke-width="1.4"/>')
    out.append(f'  <line x1="286" y1="92" x2="286" y2="{104 + 2 * 54 + s + 10}" '
               f'stroke="{INK_GHOST}" stroke-width="1"/>')
    out.append(f'  <text x="84" y="88" font-size="9.5" fill="{INK_FAINT}" '
               f'letter-spacing="1.2">SHIPPED</text>')
    out.append(f'  <text x="300" y="88" font-size="9.5" fill="{INK_FAINT}" '
               f'letter-spacing="1.2">RECOGNISED</text>')
    ly = 104 + 3 * 54 + 16
    out.append(f"""  <g>
    <rect x="28" y="{ly}" width="11" height="11" fill="{INK}"/>
    <text x="46" y="{ly + 10}" font-size="10" fill="{INK_DIM}">project shipped</text>
    <rect x="186" y="{ly}" width="11" height="11" fill="none" stroke="{INK}" stroke-width="1.3"/>
    <text x="204" y="{ly + 10}" font-size="10" fill="{INK_DIM}">recognition</text>
  </g>""")
    body = f"""{defs(uid)}
{shell(w, h)}
{starfield(w, h, 50, 606, avoid=[(20, 70, 450, 200)])}
{prompt(w, "akshat --per-year", user="akshat")}
  <text x="28" y="72" font-size="10.5" fill="{INK_FAINT}">one square = one thing · 10 shipped, 9 recognised</text>
{chr(10).join(out)}
"""
    return svg(w, h, body, base_css(), sw=("u", 14, 0.8))


# ----------------------------------------------------------------- reach --
def reach(_root):
    uid = "r"
    w, h = 490, 316
    cities = [("NEW DELHI", 150, 110, "CISCE · DST &amp; NIF", 4.0),
              ("MUMBAI", 112, 236, "IIT Bombay Techfest", 4.0),
              ("JAMSHEDPUR", 304, 152, "home · NIT JSR · CIIC", 6.5),
              ("KHARAGPUR", 374, 248, "IIT KGP · CoE AMT", 4.0)]
    hub = (304, 152)
    out = []
    for i, (_n, cx, cy, _s, _r) in enumerate(cities):
        if (cx, cy) == hub:
            continue
        d = math.hypot(cx - hub[0], cy - hub[1])
        out.append(f"""  <line x1="{hub[0]}" y1="{hub[1]}" x2="{cx}" y2="{cy}"
        stroke="{INK}" stroke-width="1" opacity="0.2"/>
  <line x1="{hub[0]}" y1="{hub[1]}" x2="{cx}" y2="{cy}" stroke="{INK}"
        stroke-width="1.6" stroke-linecap="round" opacity="0.95"
        stroke-dasharray="16 {d - 16:.0f}" filter="url(#{uid}-glow)">
    <animate attributeName="stroke-dashoffset" from="{d:.0f}" to="0"
             dur="{2.8 + i * 0.6:.1f}s" repeatCount="indefinite"/>
  </line>""")
    for i, (name, cx, cy, sub, r) in enumerate(cities):
        is_hub = (cx, cy) == hub
        out.append(f"""  <g class="pop" style="animation-delay:{0.3 + i * 0.12:.2f}s">
    <circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="none" stroke="{INK}" stroke-width="1"
            opacity="0.5">
      <animate attributeName="r" values="{r + 4};{r + 16}" dur="3.4s"
               begin="{i * 0.6:.1f}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.55;0" dur="3.4s"
               begin="{i * 0.6:.1f}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" filter="url(#{uid}-glow)"/>
    {"" if not is_hub else f'<circle cx="{cx}" cy="{cy}" r="{r + 5}" fill="none" stroke="{INK}" stroke-width="1.2"/>'}
    <text x="{cx}" y="{cy + r + 18}" text-anchor="middle" font-size="10.5"
          font-weight="bold" fill="{INK}" letter-spacing="0.8">{name}</text>
    <text x="{cx}" y="{cy + r + 31}" text-anchor="middle" font-size="8.8"
          fill="{INK_FAINT}">{sub}</text>
  </g>""")
    body = f"""{defs(uid)}
{shell(w, h)}
{starfield(w, h, 80, 3030, avoid=[(60, 85, 390, 215)])}
{prompt(w, "akshat --reach", user="akshat")}
  <text x="28" y="72" font-size="10.5" fill="{INK_FAINT}">built in Jharkhand · recognised nationally</text>
{chr(10).join(out)}
"""
    return svg(w, h, body, base_css(), sw=("r", 14, 3.2))


# -------------------------------------------------------- constellation --
def works(_root):
    """The ten projects as a star chart: an edge means a shared theme, and a
    node grows with the number of edges it carries."""
    uid = "k"
    h = 500
    nodes = {
        "Waste Mgmt":      (132, 206, "2025"),
        "GridSphere":      (292, 140, "2025–26"),
        "CarbonRoute":     (486, 110, "2026"),
        "Aegis Edge":      (676, 152, "2026"),
        "PCB Inspector":   (862, 214, "2026"),
        "Blix Bot":        (818, 368, "2024"),
        "Kinexa":          (628, 416, "2026"),
        "TS-GLDC":         (438, 384, "2026"),
        "Cyberbullying":   (258, 322, "2025"),
        "Fraud Detection": (552, 258, "2025–26"),
    }
    edges = [("GridSphere", "CarbonRoute"), ("GridSphere", "TS-GLDC"),
             ("GridSphere", "Waste Mgmt"), ("CarbonRoute", "Aegis Edge"),
             ("CarbonRoute", "Fraud Detection"), ("Aegis Edge", "PCB Inspector"),
             ("PCB Inspector", "Blix Bot"), ("Fraud Detection", "Cyberbullying"),
             ("Cyberbullying", "Kinexa"), ("Kinexa", "TS-GLDC")]
    deg = {k: 0 for k in nodes}
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    out = []
    for i, (a, b) in enumerate(edges):
        ax, ay, _ = nodes[a]
        bx, by, _ = nodes[b]
        d = math.hypot(bx - ax, by - ay)
        out.append(f"""  <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{INK}"
        stroke-width="1" opacity="0.18"/>
  <line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{INK}" stroke-width="1.5"
        stroke-linecap="round" stroke-dasharray="12 {d - 12:.0f}" opacity="0.9">
    <animate attributeName="stroke-dashoffset" from="{d:.0f}" to="0"
             dur="{3.0 + (i % 5) * 0.8:.1f}s" repeatCount="indefinite"/>
  </line>""")
    for i, (name, (x, y, yr)) in enumerate(nodes.items()):
        r = 4.5 + deg[name] * 1.5
        out.append(f"""  <g class="pop" style="animation-delay:{0.3 + i * 0.08:.2f}s">
    <circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{INK}" filter="url(#{uid}-glow)">
      <animate attributeName="opacity" values="1;0.55;1" dur="{3.4 + i * 0.3:.1f}s"
               repeatCount="indefinite"/>
    </circle>
    <text x="{x}" y="{y + r + 18:.0f}" text-anchor="middle" font-size="11"
          font-weight="bold" fill="{INK}">{name}</text>
    <text x="{x}" y="{y + r + 31:.0f}" text-anchor="middle" font-size="9"
          fill="{INK_FAINT}">{yr}</text>
  </g>""")
    body = f"""{defs(uid, 2.6)}
{shell(W, h)}
{starfield(W, h, 170, 8080, max_r=1.5)}
{prompt(W, "akshat/work --constellation")}
{chr(10).join(out)}
  <text x="28" y="{h - 18}" font-size="10" fill="{INK_FAINT}">a line joins two projects that share a theme · a node grows with the links it carries</text>
"""
    return svg(W, h, body, base_css(), sw=("k", 18, 4.0))
