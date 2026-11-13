"""Merge translation batches, generate Traditional Chinese, validate, and embed
the dictionary into src/app.html. Picks up every chunk*.json batch automatically.
Run via tools/build_all.py (or directly; paths are resolved from this file)."""
import glob, json, os, re, sys
from collections import Counter
from opencc import OpenCC

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGE = os.path.join(ROOT, "src", "app.html")

def num(path):
    m = re.search(r"chunk(\d+)\.json$", path)
    return int(m.group(1)) if m else 0

def read(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# English sources: src.json holds batches 1-2; chunkN.json holds later batches.
src = read(os.path.join(HERE, "src.json"))
for f in sorted(glob.glob(os.path.join(HERE, "chunk*.json")), key=num):
    src.update(read(f))

def load(lang):
    d = {}
    for f in sorted(glob.glob(os.path.join(HERE, f"{lang}.chunk*.json")), key=num):
        d.update(read(f))
    return d

TAG = re.compile(r"<[^>]+>"); PH = re.compile(r"\{\d+\}")
def check(d):
    bad = []
    for k, en in src.items():
        t = d.get(k)
        if not t:
            bad.append((k, "missing")); continue
        if Counter(PH.findall(en)) != Counter(PH.findall(t)): bad.append((k, "placeholder"))
        if Counter(TAG.findall(en)) != Counter(TAG.findall(t)): bad.append((k, "tags"))
    return bad

cc = OpenCC("s2tw")
# Taiwan usage fixes OpenCC gets wrong in this content (干 -> 乾 for "dry", cm -> 公分).
TW_TERMS = {"釐米": "公分", "幹血粉": "乾血粉", "變幹": "變乾"}
def tw(t):
    for k, v in TW_TERMS.items():
        t = t.replace(k, v)
    return t
def conv(s):
    return "".join(p if p.startswith("<") else tw(cc.convert(p)) for p in re.split(r"(<[^>]+>)", s))

zh = load("zh-Hans"); ms = load("ms")
langs = (("zh-Hans", zh), ("zh-Hant", {k: conv(v) for k, v in zh.items()}), ("ms", ms))
out, failed = {}, False
for lang, d in langs:
    bad = check(d)
    badids = {b[0] for b in bad}
    print(lang, len(d), "strings,", len(bad), "problems", bad[:10])
    failed |= bool(bad)
    # deterministic order; a later batch with the same English text wins
    out[lang] = {src[k]: d[k] for k in sorted(src, key=lambda x: int(x[1:])) if k in d and k not in badids}

with open(PAGE, encoding="utf-8") as f:
    s = f.read()
marker = "const I18N_DICT="
i = s.index(marker); j = s.index(";/*I18N_DATA*/", i)
data = json.dumps(out, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
s = s[:i] + marker + data + s[j:]
with open(PAGE, "w", encoding="utf-8") as f:
    f.write(s)
print("embedded", len(data.encode()), "bytes into", os.path.relpath(PAGE, ROOT))
sys.exit(1 if failed else 0)
