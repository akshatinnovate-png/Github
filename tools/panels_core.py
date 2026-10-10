"""Narrative panels: the boot log, the work tree, the timeline, the honours."""

from theme import (
    EDGE, INK, INK_DIM, INK_FAINT, INK_GHOST,
    base_css, cursor, defs, prompt, shell, starfield, svg,
)

W = 1000


# --------------------------------------------------------------- boot log --
def boot(_root):
    """`./init --all` - the about section as a service start-up trace."""
    uid = "b"
    lines = [
        ("OK", "mount  /dev/curiosity", "opened 2024 · never unmounted"),
        ("OK", "load   systems-engineering.ko", "first principles, all the way down"),
        ("OK", "start  gridsphere.service", "microgrid control · p2p energy trading"),
        ("OK", "start  pcb-inspector.service", "opencv · calibrated measurement · robot coords"),
        ("OK", "start  aegis-edge.service", "offline-first inference · crdt sync"),
        ("OK", "start  carbonroute.service", "multi-objective routing · digital twin"),
        ("OK", "attach coe-amt@iit-kharagpur", "cnn · smd + pcb trace defect detection"),
        ("OK", "attach ciic@nit-jamshedpur", "dst–nidhi · startup incubation"),
        ("OK", "grant  emergent-ventures", "mercatus center, gmu · us$9,500"),
        ("··", "start  sleep.service", "degraded"),
    ]
    step = 24
    h = 78 + len(lines) * step + 62
    out = []
    for i, (tag, cmd, detail) in enumerate(lines):
        y = 82 + i * step
        tag_ink = INK if tag == "OK" else INK_FAINT
        out.append(f"""  <g class="type" style="animation-delay:{0.25 + i * 0.13:.2f}s">
    <text x="28" y="{y}" font-size="12" fill="{INK_GHOST}">[</text>
    <text x="40" y="{y}" font-size="12" fill="{tag_ink}">{tag}</text>
    <text x="{40 + 2 * 7.2:.0f}" y="{y}" font-size="12" fill="{INK_GHOST}">]</text>
    <text x="80" y="{y}" font-size="12.5" fill="{INK}">{cmd}</text>
    <text x="392" y="{y}" font-size="11.5" fill="{INK_FAINT}">{detail}</text>
  </g>""")
    tail_y = 82 + len(lines) * step + 26
    body = f"""{defs(uid)}
{shell(W, h)}
{starfield(W, h, 90, 1234, avoid=[(20, 60, 900, h - 100)])}
{prompt(W, "./init --all")}
{chr(10).join(out)}
  <text x="28" y="{tail_y}" font-size="12.5" fill="{INK_FAINT}">akshat@jamshedpur:~$</text>
  {cursor(188, tail_y - 11, 9, 14, "2.0s")}
  <text x="{W - 28}" y="{h - 18}" text-anchor="end" font-size="9" fill="{INK_FAINT}"
        letter-spacing="1.4">10 UNITS · 9 ACTIVE · 1 DEGRADED</text>
"""
    return svg(W, h, body, base_css())


# -------------------------------------------------------------- work tree --
def tree(_root):
    """`tree ~/akshat/work` - the portfolio as a filesystem, connectors drawn
    as real strokes so no box-drawing glyph has to exist in the font."""
    uid = "w"
    groups = [
        ("energy/", [("gridsphere", "2025–26", "incubated · CIIC, NIT Jamshedpur")]),
        ("vision/", [("pcb-inspector", "2026", "IIT Kharagpur collaboration"),
                     ("blix-bot", "2024", "runner-up · Blixathon, Techfest")]),
        ("edge/", [("aegis-edge", "2026", "offline-first memory infrastructure")]),
        ("logistics/", [("carbonroute", "2026", "network-level route intelligence")]),
        ("risk/", [("fraud-detection", "2025–26", "first position · Amazon AWS"),
                   ("cyberbullying-detect", "2025", "runner-up · SparkX, IIT Bombay")]),
        ("safety/", [("ts-gldc", "2026", "INSPIRE MANAK · DST &amp; NIF India"),
                     ("kinexa", "2026", "top 40 · Samsung Solve for Tomorrow")]),
        ("sustainability/", [("waste-management", "2025", "runner-up · Design Championship")]),
    ]
    step = 23
    rows = []
    y = 82
    rows.append(("root", "~/akshat/work", "", "", y))
    y += step
    for gname, kids in groups:
        rows.append(("dir", gname, "", "", y))
        y += step
        for k, yr, note in kids:
            rows.append(("file", k, yr, note, y))
            y += step
    h = y + 48

    root_y = rows[0][4]
    dir_ys = [r[4] for r in rows if r[0] == "dir"]
    out = []

    # spine from the root down to the last top-level folder
    out.append(f'  <line x1="36" y1="{root_y + 8}" x2="36" y2="{dir_ys[-1]}" '
               f'stroke="{INK_GHOST}" stroke-width="1"/>')
    for i, r in enumerate(rows):
        kind, name, yr, note, ry = r
        if kind == "dir":
            out.append(f'  <line x1="36" y1="{ry - 4}" x2="52" y2="{ry - 4}" '
                       f'stroke="{INK_GHOST}" stroke-width="1"/>')
            kids = [q for q in rows[i + 1:] if q[0] == "file"]
            following = rows[i + 1:]
            kids = []
            for q in following:
                if q[0] == "dir":
                    break
                kids.append(q)
            if kids:
                out.append(f'  <line x1="66" y1="{ry}" x2="66" y2="{kids[-1][4] - 4}" '
                           f'stroke="{INK_GHOST}" stroke-width="1"/>')
        elif kind == "file":
            out.append(f'  <line x1="66" y1="{ry - 4}" x2="84" y2="{ry - 4}" '
                       f'stroke="{INK_GHOST}" stroke-width="1"/>')

    for i, (kind, name, yr, note, ry) in enumerate(rows):
        d = 0.2 + i * 0.055
        if kind == "root":
            out.append(f'  <text class="slide" style="animation-delay:{d:.2f}s" x="28" '
                       f'y="{ry}" font-size="13" font-weight="bold" fill="{INK}">{name}</text>')
        elif kind == "dir":
            out.append(f'  <text class="slide" style="animation-delay:{d:.2f}s" x="56" '
                       f'y="{ry}" font-size="12.5" fill="{INK_DIM}">{name}</text>')
        else:
            out.append(f"""  <g class="slide" style="animation-delay:{d:.2f}s">
    <rect x="88" y="{ry - 11}" width="5" height="5" fill="{INK}"/>
    <text x="102" y="{ry}" font-size="12.5" fill="{INK}">{name}</text>
    <text x="330" y="{ry}" font-size="11" fill="{INK_FAINT}">{yr}</text>
    <text x="404" y="{ry}" font-size="11.5" fill="{INK_DIM}">{note}</text>
  </g>""")

    body = f"""{defs(uid)}
{shell(W, h)}
{starfield(W, h, 110, 5150, avoid=[(20, 60, 900, h - 96)])}
{prompt(W, "tree ~/akshat/work --with-awards")}
{chr(10).join(out)}
  <text x="28" y="{h - 18}" font-size="9.5" fill="{INK_FAINT}">7 directories, 10 projects, 2024–2026</text>
"""
    return svg(W, h, body, base_css())


# -------------------------------------------------------------- timeline --
def experience(_root):
    uid = "e"
    rows = [
        ("OCT 2026 — PRESENT", "Mercatus Center, George Mason University",
         "Emergent Ventures Grantee",
         "US$9,500 grant · TS-GLDC passive LPG leak-detection tape", True),
        ("AUG 2026 — PRESENT", "Akshen Electric", "Intern",
         "EV two-wheeler market research, validation &amp; roadmap input", True),
        ("JAN 2026 — PRESENT", "NIT Jamshedpur · CIIC", "Incubatee",
         "Leading the smart-grid venture under the DST–NIDHI ecosystem", True),
        ("MAY 2026 — JUN 2026", "IIT Kharagpur · CoE in Adv. Mfg. Technology",
         "External Collaborator — Machine Vision Researcher",
         "Custom CNN for pixel-level SMD, MCU &amp; PCB trace defect detection", False),
    ]
    step = 92
    h = 76 + len(rows) * step + 16
    out = []
    for i, (date, org, role, note, live) in enumerate(rows):
        y = 100 + i * step
        halo = ""
        if live:
            halo = (f'<rect x="38" y="{y - 11}" width="14" height="14" fill="none" '
                    f'stroke="{INK}" stroke-width="1">'
                    f'<animate attributeName="width" values="14;26" dur="2.6s" '
                    f'begin="{i * 0.45:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="height" values="14;26" dur="2.6s" '
                    f'begin="{i * 0.45:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="x" values="38;32" dur="2.6s" '
                    f'begin="{i * 0.45:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{y - 11};{y - 17}" dur="2.6s" '
                    f'begin="{i * 0.45:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0.8;0" dur="2.6s" '
                    f'begin="{i * 0.45:.1f}s" repeatCount="indefinite"/></rect>')
        mark = (f'<rect x="38" y="{y - 11}" width="14" height="14" '
                f'fill="{INK if live else "none"}" stroke="{INK}" stroke-width="1.4"/>')
        out.append(f"""  <g class="rise" style="animation-delay:{0.25 + i * 0.15:.2f}s">
    {halo}{mark}
    <text x="72" y="{y}" font-size="10.5" fill="{INK_FAINT}" letter-spacing="1.6">{date}</text>
    <text x="72" y="{y + 23}" font-size="15" font-weight="bold" fill="{INK}">{org}</text>
    <text x="72" y="{y + 43}" font-size="13" fill="{INK_DIM}">{role}</text>
    <text x="72" y="{y + 62}" font-size="11.5" fill="{INK_FAINT}">{note}</text>
  </g>""")
    rail = (f'  <line x1="45" y1="86" x2="45" y2="{100 + (len(rows) - 1) * step - 11}" '
            f'stroke="{INK_GHOST}" stroke-width="1"/>')
    body = f"""{defs(uid)}
{shell(W, h)}
{starfield(W, h, 120, 555, avoid=[(30, 70, 760, h - 100)])}
{prompt(W, "ps --roles --current")}
{rail}
{chr(10).join(out)}
"""
    return svg(W, h, body, base_css())


# --------------------------------------------------------------- honours --
def awards(_root):
    uid = "a"
    rows = [
        ("Top 40", "Samsung Solve for Tomorrow India", "2026", "Kinexa"),
        ("INSPIRE MANAK", "DST &amp; NIF India", "2026", "TS-GLDC"),
        ("Incubated", "CIIC, NIT Jamshedpur", "2026", "GridSphere"),
        ("Emergent Ventures", "Mercatus Center, GMU · US$9,500", "2026", "TS-GLDC"),
        ("First Position", "Amazon AWS", "2025–26", "Fraud Detection"),
        ("Top 5", "Industry Academia Conclave, NIT JSR", "2025", "GridSphere"),
        ("Runner-up", "SparkX, IIT Bombay Techfest", "2025", "Cyberbullying Detection"),
        ("Runner-up", "Design Championship (ICT 360)", "2025", "Waste Mgmt Software"),
        ("Runner-up", "Blixathon, IIT Bombay Techfest", "2024", "Blix Bot"),
    ]
    h = 132 + len(rows) * 31 + 26
    out = []
    for i, (rank, where, yr, proj) in enumerate(rows):
        y = 136 + i * 31
        out.append(f"""  <g class="slide" style="animation-delay:{0.3 + i * 0.07:.2f}s">
    <rect x="30" y="{y - 9}" width="6" height="6" fill="{INK}"/>
    <text x="50" y="{y}" font-size="12.5" font-weight="bold" fill="{INK}">{rank}</text>
    <text x="210" y="{y}" font-size="12.5" fill="{INK_DIM}">{where}</text>
    <text x="620" y="{y}" font-size="11" fill="{INK_FAINT}">{yr}</text>
    <text x="{W - 28}" y="{y}" text-anchor="end" font-size="10.5" fill="{INK_FAINT}">{proj}</text>
  </g>""")
    banner = f"""  <g class="rise" style="animation-delay:.2s">
    <text x="28" y="80" font-size="15" font-weight="bold" fill="{INK}"
          filter="url(#{uid}-glow)">Youngest awardee in the history of Samsung Solve for Tomorrow India.</text>
    <text x="28" y="102" font-size="11" fill="{INK_FAINT}">Nine recognitions in three years — school robotics to a national innovation grant.</text>
  </g>
  <line x1="28" y1="117" x2="{W - 28}" y2="117" stroke="{EDGE}" stroke-width="1"/>"""
    body = f"""{defs(uid)}
{shell(W, h)}
{starfield(W, h, 130, 7007, avoid=[(20, 60, 900, h - 90)])}
{prompt(W, "cat ~/akshat/honours.log")}
{banner}
{chr(10).join(out)}
"""
    return svg(W, h, body, base_css())
