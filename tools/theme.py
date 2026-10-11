"""Shared visual language: deathly black, white stars, monospace everywhere.

Strictly monochrome. Nothing here emits a hue - series identity is carried by
position, shape and a direct label, never by colour, so the panels survive
greyscale, print and forced-colours intact.
"""

import math

BG = "#000000"
EDGE = "#1C1C1C"
EDGE_LIT = "#4C4C4C"

INK = "#FFFFFF"
INK_DIM = "#A6A6A6"
INK_FAINT = "#6B6B6B"
INK_GHOST = "#3C3C3C"

MONO = "'Courier New', ui-monospace, monospace"
ADV = 0.6          # Courier advance width, in em - lets us place glyphs exactly


class Rng:
    """Deterministic LCG so every rebuild emits byte-identical art."""

    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF

    def range(self, lo, hi):
        return lo + (hi - lo) * self.next()


def defs(uid, glow=2.2):
    return f"""  <defs>
    <filter id="{uid}-glow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="{glow}" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>"""


def shell(w, h, r=0):
    """Pure black field with a hairline frame that breathes."""
    return f"""  <rect width="{w}" height="{h}" rx="{r}" fill="{BG}"/>
  <rect class="edge" x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{r}"
        fill="none" stroke="{EDGE_LIT}" stroke-width="1"/>"""


def corners(x, y, w, h, n=16, stroke=INK, sw=1.6, op=0.9):
    """Viewfinder brackets - the reticle motif used around framed content."""
    return f"""  <g stroke="{stroke}" stroke-width="{sw}" fill="none" opacity="{op}">
    <path d="M{x} {y + n} V{y} H{x + n}"/>
    <path d="M{x + w - n} {y} H{x + w} V{y + n}"/>
    <path d="M{x + w} {y + h - n} V{y + h} H{x + w - n}"/>
    <path d="M{x + n} {y + h} H{x} V{y + h - n}"/>
  </g>"""


def starfield(w, h, n, seed, avoid=None, max_r=1.4):
    rng = Rng(seed)
    avoid = avoid or []
    out, placed, guard = [], 0, 0
    while placed < n and guard < n * 40:
        guard += 1
        x, y = rng.range(4, w - 4), rng.range(4, h - 4)
        if any(ax <= x <= ax + aw and ay <= y <= ay + ah for ax, ay, aw, ah in avoid):
            continue
        r = rng.range(0.3, max_r)
        o = rng.range(0.14, 0.85) * (0.5 + r / max_r * 0.5)
        placed += 1
        if rng.next() > 0.7:
            out.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{INK}" opacity="{o:.2f}">'
                f'<animate attributeName="opacity" values="{o:.2f};{o * 0.12:.2f};{o:.2f}" '
                f'dur="{rng.range(2.2, 6.4):.1f}s" begin="{rng.range(0, 5):.1f}s" '
                f'repeatCount="indefinite"/></circle>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" '
                       f'fill="{INK}" opacity="{o:.2f}"/>')
    return "  <g>" + "".join(out) + "</g>"


def scanlines(x, y, w, h, step=3, op=0.055):
    """CRT raster laid over framed content."""
    rows = "".join(f'<rect x="{x}" y="{yy}" width="{w}" height="1"/>'
                   for yy in range(int(y), int(y + h), step))
    return f'  <g fill="{INK}" opacity="{op}">{rows}</g>'


def prompt(w, label, y=34, user="akshat@jamshedpur"):
    """The shell prompt that heads every panel."""
    ux = 28
    cmd_x = ux + len(user + ":~$ ") * 12.5 * ADV
    return f"""  <text x="{ux}" y="{y}" font-size="12.5" fill="{INK_FAINT}">{user}:~$</text>
  <text x="{cmd_x:.0f}" y="{y}" font-size="12.5" fill="{INK}">{label}</text>
  <line x1="28" y1="{y + 14}" x2="{w - 28}" y2="{y + 14}" stroke="{EDGE}" stroke-width="1"/>
  <rect x="28" y="{y + 13}" width="58" height="1.5" fill="{INK}" opacity="0.8">
    <animate attributeName="x" values="28;{w - 86};28" dur="11s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.1;0.85;0.1" dur="11s" repeatCount="indefinite"/>
  </rect>"""


def sweep(uid, w, h, cycle=16.0, phase=0.0, band=260, peak=0.10):
    """A band of light that crosses the panel, then waits out the rest of the
    cycle off-screen. Content underneath stays fully visible the whole time -
    the sweep lights it, it never gates it."""
    cross = min(0.22, 2.6 / cycle)
    return f"""  <defs>
    <linearGradient id="{uid}-sw" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{INK}" stop-opacity="0"/>
      <stop offset="45%" stop-color="{INK}" stop-opacity="{peak}"/>
      <stop offset="55%" stop-color="{INK}" stop-opacity="{peak}"/>
      <stop offset="100%" stop-color="{INK}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect y="0" width="{band}" height="{h}" fill="url(#{uid}-sw)" x="{-band}">
    <animate attributeName="x" values="{-band};{w};{w}"
             keyTimes="0;{cross:.3f};1" dur="{cycle}s" begin="{phase}s"
             repeatCount="indefinite"/>
  </rect>
  <rect y="0" width="1.5" height="{h}" fill="{INK}" opacity="0" x="{-band}">
    <animate attributeName="x" values="0;{w};{w}" keyTimes="0;{cross:.3f};1"
             dur="{cycle}s" begin="{phase}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;.5;0;0" keyTimes="0;{cross/2:.3f};{cross:.3f};1"
             dur="{cycle}s" begin="{phase}s" repeatCount="indefinite"/>
  </rect>"""


def a11y(title, desc):
    return f"  <title>{title}</title>\n  <desc>{desc}</desc>"


def cursor(x, y, w=9, h=15, begin="0s"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK}">'
            f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" '
            f'begin="{begin}" repeatCount="indefinite"/></rect>')


def base_css(extra=""):
    """Reveal keyframes whose resting state is visible: `backwards` applies the
    hidden frame only during the delay, so a renderer that drops animation
    still shows every element."""
    return f"""  <style>
    .edge {{ animation: edge 7s ease-in-out infinite; }}
    @keyframes edge {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: .85; }} }}
    .rise {{ opacity: 1; animation: rise .5s steps(6,end) backwards; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }}
                       to   {{ opacity: 1; transform: translateY(0); }} }}
    .slide {{ opacity: 1; animation: slide .45s steps(6,end) backwards; }}
    @keyframes slide {{ from {{ opacity: 0; transform: translateX(-10px); }}
                        to   {{ opacity: 1; transform: translateX(0); }} }}
    .type {{ opacity: 1; animation: type .3s steps(2,end) backwards; }}
    @keyframes type {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .pop {{ opacity: 1; animation: pop .5s cubic-bezier(.2,.9,.3,1.1) backwards; }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.8); }}
                      to   {{ opacity: 1; transform: scale(1); }} }}
    text {{ font-family: {MONO}; }}
{extra}  </style>"""


def svg(w, h, body, css="", sw=None):
    """`sw=(uid, cycle, phase)` lays the light sweep over the finished panel."""
    if sw:
        body += "\n" + sweep(sw[0], w, h, cycle=sw[1], phase=sw[2])
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n{css}\n{body}\n</svg>\n')


def polar(cx, cy, r, deg):
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)
