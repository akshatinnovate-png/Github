"""Hero: a dithered portrait that unravels strip by strip beside the name."""

import base64

from theme import (
    ADV, EDGE, INK, INK_DIM, INK_FAINT, INK_GHOST,
    base_css, corners, cursor, defs, scanlines, shell, starfield, svg,
)

W, H = 1000, 462
PX, PY, PW, PH = 58, 76, 296, 318      # portrait frame
STRIPS = 26                             # slices the face unravels into
NAME = "AKSHAT SARKAR"
NX, NY, NSIZE = 406, 198, 52

TICKER = ("AKSHAT SARKAR / JAMSHEDPUR / SYSTEMS ENGINEERING / AI / ROBOTICS "
          "/ EDGE / 2026")


def _img(root):
    raw = (root / "assets" / "portrait.png").read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def _unravel(uid):
    """Clip each slice, then slide the clipped unit into place so the face
    assembles rather than smears."""
    sh = PH / STRIPS
    clips, body = [], []
    for i in range(STRIPS):
        y = PY + i * sh
        clips.append(
            f'    <clipPath id="{uid}-c{i}">'
            f'<rect x="{PX}" y="{y:.2f}" width="{PW}" height="{sh:.2f}"/></clipPath>')
        off = (-1 if i % 2 else 1) * (170 + (i * 53) % 230)
        body.append(
            f'    <g class="st" style="animation-delay:{0.25 + i * 0.045:.2f}s;--o:{off}px">'
            f'<g clip-path="url(#{uid}-c{i})"><use href="#{uid}-img"/></g></g>')
    return "\n".join(clips), "\n".join(body)


def build(root):
    uid = "h"
    clips, strips = _unravel(uid)
    b64 = base64.b64encode(TICKER.encode()).decode()
    name_w = len(NAME) * NSIZE * ADV

    glyphs = [
        f'    <text class="g" style="animation-delay:{0.55 + i * 0.05:.2f}s" '
        f'x="{NX + i * NSIZE * ADV:.1f}" y="{NY}" font-size="{NSIZE}" '
        f'font-weight="bold" fill="{INK}">{ch}</text>'
        for i, ch in enumerate(NAME) if ch != " "
    ]

    chips, cx = [], NX
    for i, txt in enumerate(["JAMSHEDPUR, IN",
                             "GULMOHUR HIGH SCHOOL · CLASS IX",
                             "SINCE 2024"]):
        cw = len(txt) * 6.5 + 34
        chips.append(
            f'  <g class="rise" style="animation-delay:{1.5 + i * 0.1:.2f}s">'
            f'<rect x="{cx:.0f}" y="344" width="{cw:.0f}" height="24" rx="2" '
            f'fill="none" stroke="{EDGE}" stroke-width="1"/>'
            f'<rect x="{cx + 11:.0f}" y="353" width="5" height="5" fill="{INK}"/>'
            f'<text x="{cx + 24:.0f}" y="360" font-size="9.5" fill="{INK_DIM}" '
            f'letter-spacing="0.8">{txt}</text></g>')
        cx += cw + 10

    css = base_css("""    .st { opacity: 1; animation: st .55s steps(7,end) backwards; }
    @keyframes st { from { opacity: 0; transform: translateX(var(--o)); }
                    to   { opacity: 1; transform: translateX(0); } }
    .g { opacity: 1; animation: g .28s steps(3,end) backwards; }
    @keyframes g { from { opacity: 0; } to { opacity: 1; } }
""")

    body = f"""{defs(uid)}
  <defs>
    <image id="{uid}-img" href="{_img(root)}" x="{PX}" y="{PY}"
           width="{PW}" height="{PH}" preserveAspectRatio="xMidYMid slice"/>
{clips}
  </defs>
{shell(W, H)}
{starfield(W, H, 240, 4242, avoid=[(PX - 12, PY - 12, PW + 24, PH + 24),
                                   (390, 150, 600, 230)], max_r=1.6)}

  <!-- portrait, unravelling -->
  <g>
{strips}
  </g>
{scanlines(PX, PY, PW, PH)}
{corners(PX - 10, PY - 10, PW + 20, PH + 20, 18)}
  <rect x="{PX}" y="{PY}" width="{PW}" height="2" fill="{INK}" opacity="0.5">
    <animate attributeName="y" values="{PY};{PY + PH - 2};{PY}" dur="7s"
             repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.55;0" dur="7s" repeatCount="indefinite"/>
  </rect>
  <text x="{PX}" y="{PY + PH + 30}" font-size="9" fill="{INK_FAINT}"
        letter-spacing="1.6">FIG.01 &#8212; OPERATOR &#183; 1-BIT &#183; {STRIPS} SLICES</text>

  <!-- identity -->
  <text class="type" style="animation-delay:.2s" x="{NX}" y="138" font-size="11"
        fill="{INK_FAINT}" letter-spacing="4">&#62; IDENTITY</text>
  <g filter="url(#{uid}-glow)">
{chr(10).join(glyphs)}
  </g>
  <g class="type" style="animation-delay:1.3s">{cursor(NX + name_w + 8, NY - 38, 11, 44)}</g>
  <rect class="type" style="animation-delay:1.25s" x="{NX}" y="218"
        width="{name_w:.0f}" height="1.5" fill="{INK}" opacity="0.65"/>
  <text class="rise" style="animation-delay:1.30s" x="{NX}" y="252" font-size="14"
        fill="{INK}">DeepTech Founder &#183; AI Researcher</text>
  <text class="rise" style="animation-delay:1.36s" x="{NX}" y="276" font-size="12.5"
        fill="{INK_DIM}">CoE in Advanced Manufacturing Technology, IIT Kharagpur</text>
  <text class="rise" style="animation-delay:1.42s" x="{NX}" y="312" font-size="13"
        fill="{INK}">&#8220;If AI disappeared tomorrow, I&#8217;d still be building.&#8221;</text>
{chr(10).join(chips)}

  <line x1="{NX}" y1="398" x2="{W - 28}" y2="398" stroke="{INK_GHOST}" stroke-width="1"/>
  <text x="{NX}" y="420" font-size="8.5" fill="{INK_GHOST}">{b64[:72]}</text>
  <text x="{NX}" y="434" font-size="8.5" fill="{INK_GHOST}">{b64[72:]}</text>
  <text x="{W - 28}" y="452" text-anchor="end" font-size="8.5" fill="{INK_FAINT}"
        letter-spacing="2">AS.OS &#183; v0.26</text>
"""
    return svg(W, H, body, css)
