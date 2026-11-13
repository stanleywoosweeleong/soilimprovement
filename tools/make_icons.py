"""App icon: a round soil core (three horizons) with a branching root and
mycorrhizal threads, on warm sand. Drawn at 4x and downsampled."""
from PIL import Image, ImageDraw
import os, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "icons"
os.makedirs(OUT, exist_ok=True)
SAND = (244, 235, 221); RIM = (43, 30, 18)
BANDS = [(30, 43, 33), (122, 85, 48), (185, 139, 85)]   # humus, subsoil, parent material
ROOT = (244, 235, 221); SPORE = (93, 187, 134)

def draw(size, maskable=False, rounded=True):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if maskable or not rounded:
        d.rectangle([0, 0, S, S], fill=SAND)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=SAND)
    r = S * (0.33 if maskable else 0.40)
    cx = cy = S / 2
    # soil core: draw bands, then mask to a circle
    core = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    top = cy - r
    cuts = [0.0, 0.40, 0.70, 1.0]
    for c, a, b in zip(BANDS, cuts, cuts[1:]):
        cd.rectangle([cx - r, top + 2 * r * a, cx + r, top + 2 * r * b], fill=c)
    # root system (in core coordinates, relative to r)
    def P(x, y): return (cx + x * r, cy + y * r)
    w = max(2, int(r * 0.075))
    trunk = [P(0, -1.05), P(0.02, -0.55), P(-0.03, -0.05), P(0.02, 0.45), P(0, 0.80)]
    cd.line(trunk, fill=ROOT, width=w, joint="curve")
    branches = [
        ([P(0.01, -0.45), P(-0.30, -0.22), P(-0.55, -0.05)], 0.7),
        ([P(0.02, -0.35), P(0.32, -0.12), P(0.58, 0.02)], 0.7),
        ([P(-0.02, 0.05), P(-0.28, 0.28), P(-0.42, 0.55)], 0.6),
        ([P(0.01, 0.15), P(0.30, 0.38), P(0.40, 0.62)], 0.6),
        ([P(-0.30, -0.22), P(-0.38, 0.02)], 0.45),
        ([P(0.32, -0.12), P(0.30, 0.12)], 0.45),
    ]
    for pts, k in branches:
        cd.line(pts, fill=ROOT, width=max(2, int(w * k)), joint="curve")
    # mycorrhizal spores at the root tips
    for (x, y) in [(-0.55, -0.05), (0.58, 0.02), (-0.42, 0.55), (0.40, 0.62), (-0.38, 0.02), (0.30, 0.12), (0, 0.80)]:
        rr = r * 0.075
        X, Y = P(x, y)
        cd.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=SPORE)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    im.paste(core, (0, 0), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RIM, width=max(2, int(r * 0.05)))
    return im.resize((size, size), Image.LANCZOS)

draw(192).save(f"{OUT}/icon-192.png")
draw(512).save(f"{OUT}/icon-512.png")
draw(512, maskable=True).save(f"{OUT}/icon-maskable-512.png")
draw(180, rounded=False).convert("RGB").save(f"{OUT}/apple-touch-icon.png")
draw(32).save(f"{OUT}/favicon-32.png")
draw(64).save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("icons written to", OUT)
