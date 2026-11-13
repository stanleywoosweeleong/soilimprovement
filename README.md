# Huang Soil Atlas

A single-page reference app on the soil research and field methods of **Dr. Huang Jui-chang (黄瑞彰)**, the "Soil Nutritionist" at Taiwan's Tainan District Agricultural Research and Extension Station (Tainan DARES). It was compiled for Malaysian growers attending his course in Shah Alam on 9 December 2026.

The app is available in **English, 简体中文, 繁體中文 and Bahasa Melayu**. Choose a language from the header; the choice is remembered on that device.

## What's inside

| Tab | Contents |
|---|---|
| Overview | Profile and career timeline, 1998–2026 |
| Core principles | 13 principles from his papers and interviews (fertilize by the soil, disease triangle, microbes as the "second seed", pH as the fastest lever, and more) |
| Field evidence | Trial charts: melon, bitter gourd, nematodes, root rot, salt remediation, rice rotation; an organic farm case study |
| Soil test checker | Enter a lab report (EC, pH, OM, P, K, Ca, Mg) and get a prioritized prescription, including his EC-based base-fertilizer rule |
| Symptom guide | 14 nutrient disorders and root problems: what they look like, causes, and fixes with doses |
| Recovery playbook | Nine steps from diagnosis to monitoring |
| Liquid fertilizer | His fermented High-N / High-P / High-K recipes, a drum-size calculator, and a recipe builder for swapping or leaving out ingredients |
| Works library | 41 papers, handbooks and articles with key findings |
| Glossary | 46 terms explained plainly |
| Sources | Every source used |
| Get microbes | Where to look for mycorrhizal fungi, PSB and *Bacillus* products in Malaysia (sourcing research, not Dr. Huang's recommendations) |

Yields and rates are shown per **acre** (converted from the papers' per-0.1-hectare figures).

## Using it

Open `index.html` in any modern browser; no build step or server is needed. Fonts load from Google Fonts when online and fall back to system fonts offline.

To publish with GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**.

## Repository layout

```
index.html            The app (standalone; translations embedded)
tools/make_index.py   Wraps the editing copy into a standalone index.html
i18n/                 Translation sources and tooling
  RULES.md            Translation rules and terminology table
  src.json, chunk*.json            English source strings, by batch
  zh-Hans.chunk*.json, ms.chunk*.json   Translations, by batch
  build.py            Merges batches, generates Traditional Chinese (OpenCC s2tw), validates, embeds
  extract.js, extract2.js          Collect every visible string from the page (Playwright)
```

### How translation works

The page keeps its English text as written. A small runtime layer finds each piece of visible text, replaces numbers with placeholders (`{0}`, `{1}`…), and looks up the translation, so dynamic text such as the soil checker's prescriptions is translated too. Traditional Chinese is converted from Simplified Chinese with Taiwan-standard characters.

When English text changes, re-run `extract.js` / `extract2.js` to find new strings, translate them into a new `chunkN.json` batch following `i18n/RULES.md`, then run `build.py`. New strings not yet translated show in English.

## Notes and limits

- Content is drawn from Dr. Huang's published papers, Tainan DARES handbooks and newsletters, and interviews in Harvest Farm Magazine (豐年) and NewsMarket. Points that are the compiler's interpretation are marked in the app.
- The "Get microbes" tab is independent sourcing research for Malaysia; product availability was not confirmed with suppliers.
- Translations were produced with AI assistance and checked automatically for completeness; a native-speaker review is recommended, especially for Malay.
- This is not an official publication of Tainan DARES or the Ministry of Agriculture, Taiwan.
