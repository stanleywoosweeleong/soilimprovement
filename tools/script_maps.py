"""Embed Simplified<->Traditional maps so each Chinese mode shows one script only.

hans: character map Traditional->Simplified for every Han character in the page.
hant: phrase map Simplified->Traditional (Taiwan) for every Han run outside the
      translation dictionary (static text, data, preserved Chinese labels).
Usage: python3 script_maps.py page.html
"""
import json, re, sys
from opencc import OpenCC
page = sys.argv[1]
s = open(page, encoding="utf-8").read()
t2s, s2t = OpenCC("t2s"), OpenCC("s2tw")
HAN = r"[㐀-鿿豈-﫿]"
hans = {}
for ch in set(re.findall(HAN, s)):
    c = t2s.convert(ch)
    if c != ch:
        hans[ch] = c
i = s.index("const I18N_DICT="); j = s.index(";/*I18N_DATA*/", i)
outside = s[:i] + s[j:]
m0 = outside.find("const SCRIPT_MAPS=")
if m0 >= 0:
    outside = outside[:m0] + outside[outside.index(";/*SCRIPT_MAPS*/", m0):]
hant = {}
for run in set(re.findall(HAN + "+", outside)):
    c = s2t.convert(run)
    if c != run:
        hant[run] = c
data = json.dumps({"hans": hans, "hant": hant}, ensure_ascii=False)
marker = "const SCRIPT_MAPS="
if marker in s:
    a = s.index(marker); b = s.index(";/*SCRIPT_MAPS*/", a)
    s = s[:a] + marker + data + s[b:]
else:
    s = s.replace("const I18N_DICT=", marker + data + ";/*SCRIPT_MAPS*/\nconst I18N_DICT=", 1)
open(page, "w", encoding="utf-8").write(s)
print("hans chars", len(hans), "hant phrases", len(hant))
