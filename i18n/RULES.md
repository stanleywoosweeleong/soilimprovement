# Translation rules — Huang Soil Atlas

Context: a reference web app for Malaysian farmers about Dr. Huang Jui-chang (黄瑞彰), a Taiwanese soil scientist
at the Tainan District Agricultural Research and Extension Station (Tainan DARES). Content: soil fertility, salinity
(EC), pH, organic matter, mycorrhizal fungi (AMF), phosphate-solubilizing bacteria (PSB), liquid organic fertilizer,
nutrient deficiency symptoms, melon/tomato cultivation. Audience: practical farmers. Write plainly and naturally,
like a good agricultural extension leaflet — not word-for-word.

Input: a JSON object {id: English string}. Output: a JSON object {id: translated string} with EXACTLY the same ids.

Hard rules (a script will check these):
1. Placeholders {0}, {1}, … stand for numbers. Every placeholder in the source must appear exactly once in the
   translation. You may reorder them to fit the grammar. Never write the digits yourself, never add new placeholders.
2. Keep every HTML tag exactly as written (same tag names and attributes, e.g. <b>, <i>, <br>, <small>,
   <span class="zh">, <span class="mono">, <span class="chip acc">, <i style="...">). Translate only the text between
   tags. Keep entities like &amp; &gt; &lt; as entities.
3. Text inside <span class="zh">…</span> is already Chinese. Malay: keep it unchanged. Chinese: keep it unchanged
   too (it is fine if it repeats the translated term).
4. Keep unchanged: abbreviations and symbols EC, pH, AMF, PSB, N, P, K, Ca, Mg, Fe, Zn, B, S, Na, Cd, CEC, BCF, SPAD,
   Fv/Fm, cfu, °Brix, dS/m, mg/kg, ppm, P₂O₅, K₂O, NT$, scientific names in italics (Glomus, Bacillus,
   Monosporascus, Meloidogyne, Funneliformis mosseae, Trichoderma…), crop variety names in quotes ('Arus',
   'Tainan No. 12', 'Summer Dew'…), product/organization abbreviations (MARDI, UPM, NCHU, MOA, GRB).
5. Units: "acre" → Chinese 英亩 (kg/acre → 公斤/英亩, t/acre → 吨/英亩), Malay "ekar" (kg/ekar, tan/ekar).
   "ha"/"hectare" → 公顷 / hektar. "L" litre stays L. "×" dilution: Chinese 倍 (e.g. "{0}×" → "{0} 倍"), Malay keep "×".
6. If a string is only a label/name (e.g. "Low", "High", "In range", "All", "Clear", "Expand all"), translate it
   as a short UI label.
7. Output must be valid JSON (escape double quotes inside strings as \", no trailing commas). Write it with the
   Write tool to the output path given. If the file is large you may write it in parts and merge, but the final
   file must be a single JSON object.

Terminology (use consistently):
| English | 简体中文 | Bahasa Melayu |
|---|---|---|
| Dr. Huang Jui-chang / Dr. Huang | 黄瑞彰博士 / 黄博士 | Dr. Huang Jui-chang / Dr. Huang |
| Tainan DARES / Tainan station | 台南区农业改良场 / 台南场 | Stesen Tainan (Tainan DARES) |
| Soil Nutritionist | 土壤营养师 | "Pakar Nutrisi Tanah" |
| mycorrhizal fungi (AMF) | 菌根菌 (AMF) | kulat mikoriza (AMF) |
| phosphate-solubilizing bacteria (PSB) | 溶磷菌 (PSB) | bakteria pelarut fosfat (PSB) |
| nitrogen-fixing bacteria / Rhizobium | 固氮菌 / 根瘤菌 | bakteria pengikat nitrogen / Rhizobium |
| beneficial microbes | 有益微生物 | mikrob berfaedah |
| microbial fertilizer / biofertilizer | 微生物肥料 / 生物肥料 | baja mikrob / baja bio |
| salt build-up / salinity | 盐分累积 / 盐害 | pengumpulan garam / kemasinan |
| flood leaching | 浸水洗盐 | pencucian garam dengan banjiran air |
| hardpan / plough pan | 犁底硬盘 | lapisan keras (hardpan) |
| organic matter | 有机质 | bahan organik |
| coarse-fibre organic matter | 粗纤维有机质 | bahan organik berserat kasar |
| green manure | 绿肥 | baja hijau |
| compost / vermicompost | 堆肥 / 蚓粪堆肥 | kompos / vermikompos |
| liquid organic fertilizer | 有机液肥 | baja cecair organik |
| eco-enzyme | 环保酵素 | eko-enzim |
| base fertilizer / top-dressing | 基肥 / 追肥 | baja asas / baja susulan |
| soil test / soil check-up | 土壤检测 / 土壤健检 | ujian tanah / pemeriksaan tanah |
| leaf analysis | 叶片营养诊断 | analisis daun |
| disease triangle | 病害三角 | segi tiga penyakit |
| disease-suppressive soil | 抑病土 | tanah penindas penyakit |
| continuous cropping / replant problem | 连作障碍 | masalah tanaman berterusan |
| root-knot nematode | 根瘤线虫 | nematod puru akar |
| Monosporascus root rot | 黑点根腐病 | reput akar Monosporascus |
| antagonism (nutrients) | 拮抗作用 | antagonisme nutrien |
| ground magnesium limestone (GML) / dolomite | 白云石灰 (GML) / 白云石 | kapur GML / dolomit |
| palm ash | 棕榈灰 | abu sawit |
| melon / oriental melon | 洋香瓜 / 香瓜(美浓瓜) | tembikai susu (melon) / melon oriental |
| bitter gourd | 苦瓜 | peria |
| cherry tomato | 小番茄 | tomato ceri |
| water caltrop | 菱角 | kelepong air (water caltrop) |
| greenhouse / rain shelter | 温室 / 设施 / 避雨棚 | rumah hijau / struktur pelindung hujan |
| five rights | 五适（适地、适作、适时、适量、适法） | lima "betul" |
| Field evidence / Soil test checker / Symptom guide / Recovery playbook / Liquid fertilizer / Works library / Glossary / Sources / Overview / Core principles | 田间证据 / 土壤检测分析器 / 症状指南 / 土壤修复手册 / 有机液肥 / 著作库 / 术语表 / 资料来源 / 概览 / 核心原则 | Bukti Ladang / Penyemak Ujian Tanah / Panduan Simptom / Panduan Pemulihan / Baja Cecair / Pustaka Karya / Glosari / Sumber / Gambaran Keseluruhan / Prinsip Teras |
