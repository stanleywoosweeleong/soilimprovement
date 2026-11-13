"""One command for every release:  python3 tools/build_all.py

0. tools/make_qr.py     embed the app-link QR code in src/app.html and write qr.svg
1. i18n/build.py        merge translation batches and embed them in src/app.html
2. tools/script_maps.py embed Simplified/Traditional conversion maps in src/app.html
3. tools/make_index.py  wrap src/app.html into the standalone index.html (+ PWA snippet)
4. tools/make_pwa.py    write manifest.webmanifest and sw.js; the cache version is a hash
                        of the shipped files, so users get the update prompt only when
                        something actually changed.
"""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
steps = [
    [sys.executable, os.path.join(ROOT, "tools", "make_qr.py")],
    [sys.executable, os.path.join(ROOT, "i18n", "build.py")],
    [sys.executable, os.path.join(ROOT, "tools", "script_maps.py")],
    [sys.executable, os.path.join(ROOT, "tools", "make_index.py")],
    [sys.executable, os.path.join(ROOT, "tools", "make_pwa.py"), ROOT],
]
for cmd in steps:
    print("==>", os.path.relpath(cmd[1], ROOT))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode:
        sys.exit("build failed at %s" % os.path.relpath(cmd[1], ROOT))
print("build complete")
