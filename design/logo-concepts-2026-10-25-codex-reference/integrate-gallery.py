"""Append this isolated set to shared galleries without rebuilding earlier work."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
SHARED = ROOT.parent / 'logo-concepts-2026-10-25'
prefix = '../' + ROOT.name + '/'
concepts = json.loads((ROOT / 'concepts-31-40.json').read_text())
marker = '<!-- codex-reference-31-40 -->'
own = (ROOT / 'applications.html').read_text()
tabs = re.search(r'<nav\b[^>]*>(.*?)</nav>', own, re.S).group(1)
tabs = tabs.replace('aria-selected="true" tabindex="0"', 'aria-selected="false" tabindex="-1"')
panels = '\n'.join(re.findall(r'<section\b.*?</section>', own, re.S))
panels = panels.replace('tabindex="0">', 'tabindex="0" hidden>')
panels = re.sub(r'(href|src)="((?:svg/|svg-light/|applications/)[^"]+)"', lambda m: f'{m[1]}="{prefix}{m[2]}"', panels)

for filename in ['applications.html', 'index.html']:
    target = SHARED / filename
    before = target.read_text()
    if marker in before:
        print(filename + ': already integrated')
        continue
    assert 'concept-30' in before and 'concept-31' not in before
    if filename == 'applications.html':
        after = before.replace('</nav>', marker + tabs + '</nav>', 1)
        after = after.replace('</main>', marker + panels + '</main>', 1)
        after = after.replace('Навeдите мышку', 'Наведите мышку')
        after = after.replace('Наведите мышку', '31–40 — новый набор по референсу. Наведите мышку', 1)
        after = after.replace('Скачать все SVG и макеты ↓', 'Скачать наборы 01–30 ↓', 1)
        download = f' <a class="download" href="{prefix}tatsi-in-motion-31-40.zip" download>Скачать новый набор 31–40 ↓</a>'
        after = after.replace('<nav role="tablist"', download + '<nav role="tablist"', 1)
    else:
        cards = [marker + '<h2 class="set-divider" style="grid-column:1/-1;margin:26px 0 4px;font-size:14px;font-weight:500;letter-spacing:.08em;color:#bcf7f3">31–40 · новый набор по референсу</h2>']
        for c in concepts:
            n, slug = c['slug'][:2], c['slug']
            cards.append(f'''<article class="concept" id="concept-{n}"><div class="card-top"><span class="number">{n}</span><span>{c['type']}</span></div>
<div class="art"><img src="{prefix}svg/{slug}.svg" alt="{c['ru']}" width="512" height="512"></div>
<div class="card-bottom"><div><h2>{c['name']}</h2><p class="ru">{c['ru']}</p></div><a href="{prefix}svg/{slug}.svg" download>SVG ↓</a></div>
<p class="rationale">{c['idea']}</p><p style="margin:14px 0 0;font-size:12px"><a href="applications.html#concept-{n}" style="color:#bcf7f3;text-decoration:none">Сайт + Instagram →</a></p></article>''')
        after = before.replace('</article></section>', '</article>' + '\n'.join(cards) + '</section>', 1)
        assert after != before
        after = after.replace('30 logo concepts', '40 logo concepts').replace('Logo exploration / 01—30', 'Logo exploration / 01—40')
        after = after.replace('30 знаков в трёх наборах', '40 знаков в четырёх наборах').replace('все 30 вариантов', 'все 40 вариантов').replace('aria-label="30 вариантов', 'aria-label="40 вариантов')
        after = after.replace('Скачать 30 SVG ↓', 'Скачать SVG 01–30 ↓')
    assert target.read_text() == before, 'Concurrent edit detected; reread before integrating'
    target.write_text(after)
    print(filename + ': appended 31–40; earlier panels preserved')
