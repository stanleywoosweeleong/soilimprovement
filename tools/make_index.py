"""Wrap the artifact page (no <html>/<head>/<body>) into a standalone index.html."""
import sys, os
PWA = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwa_snippet.html"), encoding="utf-8").read()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "src", "app.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "index.html")
if "<!doctype" in open(src, encoding="utf-8").read(200).lower():
    sys.exit("make_index: %s is already a wrapped page; pass the editing source src/app.html" % src)
s = open(src, encoding="utf-8").read()
cut = s.index("</style>") + len("</style>")
head, body = s[:cut], s[cut:]
page = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="Dr. Huang Jui-chang\'s soil research and soil recovery methods, in English, Simplified Chinese, Traditional Chinese and Malay.">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<meta name="theme-color" content="#2B2119" media="(prefers-color-scheme: light)">\n'
    '<meta name="theme-color" content="#120D09" media="(prefers-color-scheme: dark)">\n'
    '<link rel="icon" href="icons/favicon.ico" sizes="any">\n'
    '<link rel="icon" href="icons/favicon-32.png" type="image/png" sizes="32x32">\n'
    '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-title" content="土壤修复">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    + head +
    '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>\n'
    '</head>\n<body>\n' + body + '\n' + PWA + '\n</body>\n</html>\n'
)
open(out, "w", encoding="utf-8").write(page)
print("wrote", out, len(page.encode()), "bytes")
