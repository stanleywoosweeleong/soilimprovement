"""Generate the app's QR code (link to the GitHub Pages site).

Writes qr.svg (print-ready, black on white) and embeds the same code inline in
src/app.html between <!--QR--> and <!--/QR--> so it also works offline."""
import os, re
import segno
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://stanleywoosweeleong.github.io/soilimprovement/"
BORDER = 2
q = segno.make(URL, error="m")
rows = [list(r) for r in q.matrix]
n = len(rows) + 2 * BORDER
path = []
for y, row in enumerate(rows):
    x = 0
    while x < len(row):
        if row[x]:
            start = x
            while x < len(row) and row[x]:
                x += 1
            path.append("M%d %dh%dv1h-%dz" % (start + BORDER, y + BORDER, x - start, x - start))
        else:
            x += 1
d = "".join(path)
inline = ('<svg class="qr" viewBox="0 0 %d %d" role="img" aria-label="QR code: %s" shape-rendering="crispEdges">'
          '<rect width="%d" height="%d" fill="#fff"/><path d="%s" fill="#000"/></svg>') % (n, n, URL, n, n, d)
with open(os.path.join(ROOT, "qr.svg"), "w", encoding="utf-8") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" shape-rendering="crispEdges">'
            '<rect width="%d" height="%d" fill="#fff"/><path d="%s" fill="#000"/></svg>\n' % (n, n, n * 10, n * 10, n, n, d))
page = os.path.join(ROOT, "src", "app.html")
s = open(page, encoding="utf-8").read()
s2 = re.sub(r"<!--QR-->.*?<!--/QR-->", "<!--QR-->" + inline + "<!--/QR-->", s, count=1, flags=re.S)
if s2 == s and "<!--QR-->" not in s:
    raise SystemExit("make_qr: <!--QR--> marker not found in src/app.html")
open(page, "w", encoding="utf-8").write(s2)
print("QR version", q.version, "for", URL)
