"""Regenerate every SVG panel in assets/. Run: python3 -I tools/build.py"""
import pathlib, re, sys

ENTITY_RE = re.compile(r"&(?!(?:amp|lt|gt|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)")
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import panels_hero, panels_core, panels_viz, panels_text

PANELS = [
    ("hero.svg",       panels_hero.build),
    ("metrics.svg",    panels_viz.metrics),
    ("manifest.svg",   panels_text.manifest),
    ("boot.svg",       panels_core.boot),
    ("tree.svg",       panels_core.tree),
    ("works.svg",      panels_viz.works),
    ("dossier.svg",    panels_text.dossier),
    ("meter.svg",      panels_viz.meter),
    ("units.svg",      panels_viz.units),
    ("reach.svg",      panels_viz.reach),
    ("experience.svg", panels_core.experience),
    ("awards.svg",     panels_core.awards),
    ("repos.svg",      panels_text.repos),
    ("contact.svg",    panels_text.contact),
]

CHIPS = ["PORTFOLIO", "LINKEDIN", "EMAIL",
         "AegisEdge", "CarbonRouteX", "Mercury", "CareGraph",
         "IndiaScored", "CaseD", "FocusList", "PortfolioWeb"]

def strip(text):
    """Resting state only - what a renderer without animation support shows."""
    text = re.sub(r"animation:[^;}]*;", "", text)
    text = re.sub(r"animation-delay:[^;\"}]*;?", "", text)
    for tag in ("animate", "animateTransform", "animateMotion"):
        text = re.sub(rf"<{tag}\b[^>]*/>", "", text)
    return text


def main():
    static = "--static" in sys.argv
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "assets"
    out.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, fn in PANELS:
        text = fn(ROOT)
        if static:  # resting state only, for layout review
            text = strip(text)
        bad = [m.start() for m in ENTITY_RE.finditer(text)]
        if bad:
            raise SystemExit(f"{name}: {len(bad)} unescaped '&' at {bad[:5]}")
        (out / name).write_text(text)
        n = len(text.encode()); total += n
        print(f"  {name:18s} {n:>9,d} bytes")
    cdir = out / "chips"
    cdir.mkdir(exist_ok=True)
    for label in CHIPS:
        text = panels_text.chip(label)
        if static:
            text = strip(text)
        f = cdir / (label.lower() + ".svg")
        f.write_text(text)
        total += len(text.encode())
    print(f"  {'chips/ (' + str(len(CHIPS)) + ')':18s} {sum(len((cdir / (c.lower() + '.svg')).read_text().encode()) for c in CHIPS):>9,d} bytes")
    print(f"  {'TOTAL':18s} {total:>9,d} bytes")

main()
