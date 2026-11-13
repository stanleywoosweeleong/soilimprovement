"""Wrap the artifact page (no <html>/<head>/<body>) into a standalone index.html."""
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
cut = s.index("</style>") + len("</style>")
head, body = s[:cut], s[cut:]
page = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="Dr. Huang Jui-chang\'s soil research and soil recovery methods, in English, Simplified Chinese, Traditional Chinese and Malay.">\n'
    + head +
    '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>\n'
    '</head>\n<body>\n' + body + '\n</body>\n</html>\n'
)
open(out, "w", encoding="utf-8").write(page)
print("wrote", out, len(page.encode()), "bytes")
