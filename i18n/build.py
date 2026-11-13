import json,re,sys
from collections import Counter
from opencc import OpenCC
src=json.load(open('src.json'));src.update(json.load(open('chunk3.json')));src.update(json.load(open('chunk4.json')));src.update(json.load(open('chunk5.json')));src.update(json.load(open('chunk6.json')));src.update(json.load(open('chunk7.json')))
def load(lang):
    d={}
    for n in (1,2,3,4,5,6,7):
        import os
        if not os.path.exists(f'{lang}.chunk{n}.json'): continue
        d.update(json.load(open(f'{lang}.chunk{n}.json',encoding='utf-8')))
    return d
TAG=re.compile(r'<[^>]+>');PH=re.compile(r'\{\d+\}')
def check(lang,d):
    bad=[]
    for k,en in src.items():
        t=d.get(k)
        if not t: bad.append((k,'missing'));continue
        if Counter(PH.findall(en))!=Counter(PH.findall(t)): bad.append((k,'placeholder'))
        if Counter(TAG.findall(en))!=Counter(TAG.findall(t)): bad.append((k,'tags'))
    return bad
out={}
zh=load('zh-Hans');ms=load('ms')
cc=OpenCC('s2tw')
# convert text only, never tags
TW_TERMS={'釐米':'公分'}
def tw(t):
    for k,v in TW_TERMS.items(): t=t.replace(k,v)
    return t
def conv(s): return ''.join(p if p.startswith('<') else tw(cc.convert(p)) for p in re.split(r'(<[^>]+>)',s))
zht={k:conv(v) for k,v in zh.items()}
for lang,d in (('zh-Hans',zh),('zh-Hant',zht),('ms',ms)):
    bad=check(lang,d)
    print(lang,len(d),'problems',len(bad),bad[:10])
    out[lang]={src[k]:v for k,v in d.items() if k in src and (k,'missing') not in bad and not any(b[0]==k for b in bad)}
json.dump(out,open('dict.json','w'),ensure_ascii=False)
page='../index.html';s=open(page,encoding='utf-8').read()
marker='const I18N_DICT='
i=s.index(marker);j=s.index(';/*I18N_DATA*/',i)
s=s[:i]+marker+json.dumps(out,ensure_ascii=False).replace('</','<\\/')+s[j:]
open(page,'w',encoding='utf-8').write(s)
print('embedded bytes',len(json.dumps(out,ensure_ascii=False).encode()))
