"""Panels that replace the plain-markdown sections: the manifesto, the project
dossier, the repository listing, the sign-off, and the clickable link chips."""

from theme import (
    EDGE, INK, INK_DIM, INK_FAINT, INK_GHOST,
    a11y, base_css, corners, cursor, defs, prompt, shell, starfield, sweep, svg,
)

W = 1000


# -------------------------------------------------------------- manifesto --
def manifest(_root):
    """`cat ~/akshat/README` - the about section, typed."""
    uid = "mf"
    para = [
        ("In 2024 I started building because I wanted to understand how systems", INK),
        ("actually work. That curiosity took me from software into AI, machine", INK),
        ("learning, computer vision, robotics, embedded systems, edge computing,", INK),
        ("distributed systems and systems engineering.", INK),
        ("", INK),
        ("I work across Python, TypeScript, C++, Rust, JavaScript and ONNX — from", INK_DIM),
        ("model training and computer vision to APIs, real-time systems, robotic", INK_DIM),
        ("control and edge inference.", INK_DIM),
        ("", INK),
        ("What keeps me interested is the boundary between computation and the", INK_DIM),
        ("physical world, where algorithms, hardware and real constraints all have", INK_DIM),
        ("to work together. I go deep into the stack, build from first principles,", INK_DIM),
        ("and turn ideas into working systems.", INK_DIM),
    ]
    quote = [
        "Not a demo. My projects don't set out to show off a technology — they",
        "treat resource distribution, operational efficiency, reliability,",
        "sustainability and automation as a systems problem.",
    ]
    step = 21
    top = 82
    h = top + len(para) * step + 30 + len(quote) * 20 + 56
    out = []
    for i, (line, col) in enumerate(para):
        if not line:
            continue
        out.append(f'  <text class="type" style="animation-delay:{0.2 + i * 0.1:.2f}s" '
                   f'x="28" y="{top + i * step}" font-size="13" fill="{col}">{line}</text>')
    qy = top + len(para) * step + 22
    out.append(f'  <rect x="28" y="{qy - 16}" width="2" height="{len(quote) * 20 + 4}" '
               f'fill="{INK}" opacity="0.65"/>')
    for i, line in enumerate(quote):
        bold = ' font-weight="bold"' if i == 0 else ""
        out.append(f'  <text class="type" style="animation-delay:{1.6 + i * 0.12:.2f}s" '
                   f'x="46" y="{qy + i * 20}" font-size="12.5" fill="{INK_DIM}"{bold}>{line}</text>')
    tail = qy + len(quote) * 20 + 26
    out.append(f'  <text x="28" y="{tail}" font-size="12.5" fill="{INK_FAINT}">akshat@jamshedpur:~$</text>')
    out.append("  " + cursor(188, tail - 11, 9, 14, "2.4s"))
    body = f"""{defs(uid)}
{a11y("About Akshat Sarkar",
      "A terminal panel: Akshat started building in 2024 out of curiosity about how "
      "systems work, moving from software into AI, computer vision, robotics, embedded "
      "systems and edge computing, and treats each project as a systems problem.")}
{shell(W, h)}
{starfield(W, h, 95, 1777, avoid=[(20, 62, 900, h - 100)])}
{prompt(W, "cat ~/akshat/README")}
{chr(10).join(out)}
{sweep(uid, W, h, cycle=17, phase=1.0)}
"""
    return svg(W, h, body, base_css())


# ---------------------------------------------------------------- dossier --
PROJECTS = [
    ("01", "GridSphere", "Smart AI Microgrid", "2025–26",
     "AI-enabled microgrid for regulation, fault and surge prevention, energy distribution and",
     "peer-to-peer energy trading.", "Top 5, NIT Jamshedpur · incubated at CIIC"),
    ("02", "CarbonRoute", "Logistics Intelligence", "2026",
     "Network-level transport optimisation across fleets, orders and depots over time, cost,",
     "emissions, distance and reliability — Pareto optimisation, digital-twin disruption testing.", ""),
    ("03", "PCB Inspector", "Industrial Vision", "2026",
     "OpenCV and HD camera inspection: configurable grid scanning, calibrated measurement and",
     "component coordinates streamed live to robotic systems.", "In collaboration with IIT Kharagpur"),
    ("04", "Aegis Edge", "Offline-First Edge AI", "2026",
     "Local inference with durable memory, peer reconciliation, policy-controlled data movement",
     "and autonomous degradation and recovery.", ""),
    ("05", "Fraud Detection", "E-Commerce Risk", "2025–26",
     "Treats fraudulent product returns as a risk-analysis problem, surfacing suspicious",
     "behaviour and transaction patterns.", "First Position, Amazon AWS"),
    ("06", "TS-GLDC", "LPG Leak Detection", "2026",
     "Low-cost passive safety tape that detects gas leakage without batteries or electronic",
     "sensors.", "INSPIRE MANAK, DST &amp; NIF India · Emergent Ventures grant"),
    ("07", "Kinexa", "Assistive Technology", "2026",
     "A communication bridge for deaf athletes.", "",
     "Top 40, Samsung Solve for Tomorrow India 2026"),
    ("08", "Waste Management", "Environmental Software", "2025",
     "Software for waste segregation across categories.", "",
     "Runner-up, Design Championship 2025 (ICT 360)"),
    ("09", "Cyberbullying Detection", "Applied ML", "2025",
     "Web and ML early-warning layer for identifying potentially harmful online interactions.", "",
     "Runner-up, SparkX, IIT Bombay Techfest 2025"),
    ("10", "Blix Bot", "Mobile Robotics", "2024",
     "Mobile football-playing robot.", "",
     "Runner-up, Best Innovation, Blixathon, IIT Bombay Techfest 2024"),
]


def dossier(_root):
    uid = "ds"
    top = 84
    out, y = [], top
    for i, (idx, name, sub, yr, d1, d2, award) in enumerate(PROJECTS):
        d = 0.2 + i * 0.12
        out.append(f"""  <g class="slide" style="animation-delay:{d:.2f}s">
    <text x="28" y="{y}" font-size="11" fill="{INK_GHOST}">{idx}</text>
    <text x="58" y="{y}" font-size="14" font-weight="bold" fill="{INK}">{name}</text>
    <text x="{58 + len(name) * 8.4 + 14:.0f}" y="{y}" font-size="11.5"
          fill="{INK_FAINT}">{sub}</text>
    <text x="{W - 28}" y="{y}" text-anchor="end" font-size="10.5"
          fill="{INK_FAINT}">{yr}</text>
    <text x="58" y="{y + 19}" font-size="11.5" fill="{INK_DIM}">{d1}</text>""")
        yy = y + 19
        if d2:
            yy += 17
            out.append(f'    <text x="58" y="{yy}" font-size="11.5" fill="{INK_DIM}">{d2}</text>')
        if award:
            yy += 18
            out.append(f'    <rect x="58" y="{yy - 8}" width="5" height="5" fill="{INK}"/>'
                       f'<text x="72" y="{yy}" font-size="11" fill="{INK}">{award}</text>')
        out.append("  </g>")
        y = yy + 30
        if i < len(PROJECTS) - 1:
            out.append(f'  <line x1="28" y1="{y - 17}" x2="{W - 28}" y2="{y - 17}" '
                       f'stroke="{INK_GHOST}" stroke-width="1" opacity="0.6"/>')
    h = y + 14
    body = f"""{defs(uid)}
{a11y("Selected work: ten projects, 2024 to 2026",
      "A dossier of ten engineering projects with year, description and recognition: "
      "GridSphere, CarbonRoute, PCB Inspector, Aegis Edge, Fraud Detection, TS-GLDC, "
      "Kinexa, Waste Management, Cyberbullying Detection and Blix Bot.")}
{shell(W, h)}
{starfield(W, h, 150, 9123, avoid=[(20, 62, 900, h - 90)])}
{prompt(W, "akshat/work --dossier --verbose")}
{chr(10).join(out)}
{sweep(uid, W, h, cycle=22, phase=3.0)}
"""
    return svg(W, h, body, base_css())


# ------------------------------------------------------------------ repos --
REPOS = [
    ("AegisEdge", "python", "offline-first edge memory on Qdrant · CRDT sync · 392 tests"),
    ("CarbonRouteX", "javascript", "logistics intelligence across time, cost, capacity, carbon"),
    ("Mercury", "javascript", "on-device ASL fingerspelling · 20k-param model in ONNX"),
    ("CareGraph", "python", "medical records as an evidence-linked timeline, verified in-browser"),
    ("IndiaScored", "typescript", "credit risk from alternative data · SHAP + LLM explanations"),
    ("CaseD", "html", "turns a repository into a rendered trailer, locally"),
    ("FocusLIst---Exp", "html", "minimalist task management built around prioritisation"),
    ("PortfolioWeb", "html", "source of the portfolio site"),
]


def repos(_root):
    uid = "rp"
    top, step = 86, 30
    h = top + len(REPOS) * step + 44
    out = []
    for i, (name, lang, desc) in enumerate(REPOS):
        y = top + i * step
        out.append(f"""  <g class="slide" style="animation-delay:{0.2 + i * 0.1:.2f}s">
    <text x="28" y="{y}" font-size="11" fill="{INK_GHOST}">drwxr-xr-x</text>
    <text x="132" y="{y}" font-size="11" fill="{INK_FAINT}">{lang}</text>
    <text x="238" y="{y}" font-size="13" font-weight="bold" fill="{INK}">{name}</text>
    <text x="446" y="{y}" font-size="11.5" fill="{INK_DIM}">{desc}</text>
  </g>""")
    body = f"""{defs(uid)}
{a11y("Public repositories",
      "A directory listing of eight public repositories with language and purpose: "
      "AegisEdge, CarbonRouteX, Mercury, CareGraph, IndiaScored, CaseD, FocusList "
      "and PortfolioWeb.")}
{shell(W, h)}
{starfield(W, h, 85, 4545, avoid=[(20, 62, 900, h - 90)])}
{prompt(W, "ls -la ~/github/akshatinnovate-png")}
{chr(10).join(out)}
  <text x="28" y="{h - 18}" font-size="9.5" fill="{INK_FAINT}">8 public repositories · click any name below to open it</text>
{sweep(uid, W, h, cycle=19, phase=5.0)}
"""
    return svg(W, h, body, base_css())


# ---------------------------------------------------------------- sign-off --
def contact(_root):
    uid = "ct"
    h = 212
    body = f"""{defs(uid, 3.2)}
{a11y("Contact Akshat Sarkar",
      "Sign-off panel: let's build the next system. Reach Akshat at "
      "akshat.innovate@gmail.com, via the portfolio site, or on LinkedIn. "
      "Based in Jamshedpur, Jharkhand, India.")}
{shell(W, h)}
{starfield(W, h, 150, 6161, max_r=1.7)}
  <text class="rise" style="animation-delay:.2s" x="{W / 2}" y="76"
        text-anchor="middle" font-size="11" fill="{INK_FAINT}" letter-spacing="4">&#62; TRANSMIT</text>
  <text class="rise" style="animation-delay:.35s" x="{W / 2}" y="118"
        text-anchor="middle" font-size="27" font-weight="bold" fill="{INK}"
        filter="url(#{uid}-glow)">LET&#8217;S BUILD THE NEXT SYSTEM.</text>
  <text class="rise" style="animation-delay:.5s" x="{W / 2}" y="146"
        text-anchor="middle" font-size="12.5" fill="{INK_DIM}">akshat.innovate@gmail.com</text>
  <line x1="340" y1="166" x2="660" y2="166" stroke="{INK_GHOST}" stroke-width="1"/>
  <text x="{W / 2}" y="188" text-anchor="middle" font-size="9.5" fill="{INK_FAINT}"
        letter-spacing="2.2">JAMSHEDPUR &#183; JHARKHAND &#183; INDIA &#183; MADE WITH LOVE</text>
{sweep(uid, W, h, cycle=13, phase=0.5, peak=0.13)}
"""
    return svg(W, h, body, base_css())


# ------------------------------------------------------------------ chips --
def chip(label, width=None, height=42):
    """A small clickable button - the markdown wraps each one in an anchor."""
    uid = "c" + "".join(ch for ch in label.lower() if ch.isalnum())[:8]
    w = width or int(len(label) * 8.4 + 48)
    body = f"""{defs(uid, 2.0)}
{a11y(label, f"Button linking to {label}.")}
  <rect width="{w}" height="{height}" fill="#000000"/>
{corners(1, 1, w - 2, height - 2, 10, INK, 1.3, 0.85)}
  <rect x="18" y="{height / 2 - 2.5}" width="5" height="5" fill="{INK}">
    <animate attributeName="opacity" values="1;.2;1" dur="2.6s" repeatCount="indefinite"/>
  </rect>
  <text x="33" y="{height / 2 + 4.5}" font-size="12" font-weight="bold" fill="{INK}"
        letter-spacing="1.4">{label}</text>
{sweep(uid, w, height, cycle=9, phase=0.0, band=90, peak=0.16)}
"""
    return svg(w, height, body, base_css())
