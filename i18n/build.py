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

# Co-authors' names as printed in the Tainan DARES publication indexes (Traditional originals).
# Chinese text must use these, not the romanised forms used in English and Malay.
NAMES = [  # (romanised forms, longest first), Simplified, Traditional
    (["Chiang Wen-chin", "Chiang W.C.", "Chiang"], "江汶锦", "江汶錦"),
    (["Pan Chia-chen", "Pan"], "潘佳辰", "潘佳辰"),
    (["Yang Shao-jung"], "杨绍荣", "楊紹榮"),
    (["Yang Ching-fu"], "杨清富", "楊清富"),
    (["Huang Shan-nei"], "黄山内", "黃山內"),
    (["Huang Yu-ming"], "黄裕铭", "黃裕銘"),
    (["Huang Han-ling"], "黄涵灵", "黃涵靈"),
    (["Huang Yuan-man"], "黄圆满", "黃圓滿"),
    (["Lin Chin-ching", "Lin C.C."], "林晋卿", "林晉卿"),
    (["Lin Ching-wei", "Lin C.W."], "林经伟", "林經偉"),
    (["Lin Kuo-tzu"], "林国词", "林國詞"),
    (["Cho Chia-jung", "Cho C.J."], "卓家荣", "卓家榮"),
    (["Chen Shao-chung"], "陈绍崇", "陳紹崇"),
    (["Mao Jen-chieh", "Mao"], "毛壬杰", "毛壬杰"),
    (["Chang Chun-chun"], "张淳淳", "張淳淳"),
    (["Liu Yi-chang"], "刘依昌", "劉依昌"),
    (["Cheng An-hsiu"], "郑安秀", "鄭安秀"),
    (["Sun Wen-chang"], "孙文章", "孫文章"),
    (["Tseng Yi-ling"], "曾怡陵", "曾怡陵"),
]
NAME_RES = [(re.compile(r"(?<![A-Za-z])" + re.escape(f) + r"(?![A-Za-z])"), hans, hant)
            for forms, hans, hant in NAMES for f in forms]
def chinese_names(text, trad):
    out = []
    for part in re.split(r"(<[^>]+>)", text):
        if not part.startswith("<"):
            for rx, hans, hant in NAME_RES:
                part = rx.sub(hant if trad else hans, part)
            part = re.sub(r"([\u4e00-\u9fff]) (等|著|采访|採訪)", r"\1\2", part)
            part = re.sub(r"(《[丰豐]年》(?:[杂雜][志誌])?)\s*[（(][丰豐]年[）)]", r"\1", part)  # name already given
        out.append(part)
    return "".join(out)

zh = load("zh-Hans"); ms = load("ms")
langs = (("zh-Hans", {k: chinese_names(v, False) for k, v in zh.items()}),
         ("zh-Hant", {k: chinese_names(conv(v), True) for k, v in zh.items()}),
         ("ms", ms))
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
