"""Build only the isolated reference set; existing designs are read-only templates."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / 'logo-concepts-2026-10-25'
concepts = json.loads((ROOT / 'concepts-31-40.json').read_text())
bounds = {r['file']: r['bounds'] for r in json.loads((ROOT / 'verification-31-40.json').read_text())['files']}
template = (PREVIOUS / 'applications/01-flowing-t.html').read_text()
assert len(re.findall(r'<svg\b.*?</svg>', template, re.S)) == 6

def symbol(concept, instance):
    svg = (ROOT / 'svg' / (concept['slug'] + '.svg')).read_text()
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    box = bounds[concept['slug'] + '.svg']
    viewbox = f"{box['x']-20:.3f} {box['y']-20:.3f} {box['width']+40:.3f} {box['height']+40:.3f}"
    svg = re.sub(r'viewBox="[^"]+"', f'viewBox="{viewbox}"', svg)
    prefix = f"{concept['slug']}-{instance}-"
    svg = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{prefix}{m[1]}"', svg)
    svg = re.sub(r'aria-labelledby="([^"]+)"', lambda m: 'aria-labelledby="' + ' '.join(prefix + value for value in m[1].split()) + '"', svg)
    return svg

for c in concepts:
    number = c['slug'][:2]
    instances = iter(['hero', 'site', 'avatar', 'post', 'photo', 'mini'])
    board = re.sub(r'<svg\b.*?</svg>', lambda _: symbol(c, next(instances)), template, flags=re.S)
    board = board.replace('01 · Flowing T', f"{number} · {c['name']}")
    board = board.replace('Tatsi in motion / 01 of 10', f'Tatsi in motion / reference collection / {number}')
    board = board.replace('<h1>Flowing T</h1>', f"<h1>{c['name']}</h1>")
    board = re.sub(r'<p class="concept-note">.*?</p>', f'<p class="concept-note">{html.escape(c["idea"])}</p>', board)
    board = board.replace('Вариант 01 · Пластичная T', f"Вариант {number} · {c['ru']}")
    (ROOT / 'applications' / (c['slug'] + '.html')).write_text(board)

source_gallery = (PREVIOUS / 'applications.html').read_text()
style = re.search(r'<style>(.*?)</style>', source_gallery, re.S).group(1)
tabs, panels = [], []
for index, c in enumerate(concepts):
    number, slug = c['slug'][:2], c['slug']
    tabs.append(f'<a href="#concept-{number}" id="tab-{number}" role="tab" aria-controls="panel-{number}" aria-selected="{str(index == 0).lower()}" tabindex="{0 if index == 0 else -1}">{number}</a>')
    hidden = '' if index == 0 else ' hidden'
    panels.append(f'''<section id="panel-{number}" role="tabpanel" aria-labelledby="tab-{number}" tabindex="0"{hidden}>
<div class="section-title"><h2>{number} / {c['name']}</h2><a href="svg/{slug}.svg" download>Скачать SVG ↓</a></div>
<a href="applications/{slug}-board.png" target="_blank"><img src="applications/{slug}-board.png" alt="{c['ru']}: сайт и Instagram" width="1600" height="1200"></a>
<div class="links"><a href="svg-light/{slug}.svg" download>SVG для светлого фона ↓</a><a href="applications/{slug}-website.png" target="_blank">Сайт отдельно ↗</a><a href="applications/{slug}-instagram.png" target="_blank">Instagram отдельно ↗</a><a href="applications/{slug}.html" target="_blank">Макет HTML ↗</a></div></section>''')

gallery = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tatsi in motion — 10 новых вариантов по референсу</title><style>{style}</style></head><body><main>
<a href="../logo-concepts-2026-10-25/index.html">← Общая коллекция</a><h1>Линия. Буква. Движение.</h1>
<p class="intro">10 новых вариантов по вашему референсу — 31–40. Каллиграфические t, антиквенные T, открытые орбиты и мятные ленты.<br>Наведите мышь на номер: ниже появится один выбранный вариант на сайте и в Instagram. На телефоне нажмите на номер.</p>
<a class="download" href="tatsi-in-motion-31-40.zip" download>Скачать 10 SVG и все макеты ↓</a> <a href="preview/reference-31-40.png" target="_blank">Обзор десяти знаков ↗</a>
<nav role="tablist" aria-label="Выбрать новый вариант">{''.join(tabs)}</nav>{''.join(panels)}</main><script src="applications.js"></script></body></html>'''
(ROOT / 'applications.html').write_text(gallery)
(ROOT / 'index.html').write_text(gallery)
(ROOT / 'applications.js').write_text((PREVIOUS / 'applications.js').read_text())
print('Built 10 isolated application boards and a hover gallery.')
