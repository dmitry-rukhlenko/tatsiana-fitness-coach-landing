"""Add the Claude reference-led set 21-30 to this page, in front of 31-40, without rebuilding anything.

The 21-30 masters, boards and PNGs live in ../logo-concepts-2026-10-25/ (built by build-21-30.py and
build-applications-11-20.py there); this script only links them and writes dark-surface SVG copies.
Idempotent: a marker comment guards both page files.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
SHARED = ROOT.parent / 'logo-concepts-2026-10-25'
prefix = '../' + SHARED.name + '/'
concepts = json.loads((SHARED / 'concepts-21-30.json').read_text())
marker = '<!-- claude-reference-21-30 -->'

# Dark-surface versions (ink -> white, deep mint -> brand mint), the counterpart of this folder's svg-light/.
dark_dir = SHARED / 'svg-dark'
dark_dir.mkdir(exist_ok=True)
for c in concepts:
    svg = (SHARED / 'svg' / (c['slug'] + '.svg')).read_text()
    for src, dst in c.get('on_dark', {}).items():
        svg = re.sub(re.escape(src), dst, svg, flags=re.IGNORECASE)
    (dark_dir / (c['slug'] + '.svg')).write_text(svg)

tabs = ''.join(
    f'<a href="#concept-{c["slug"][:2]}" id="tab-{c["slug"][:2]}" role="tab" aria-controls="panel-{c["slug"][:2]}" '
    f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{c["slug"][:2]}</a>'
    for i, c in enumerate(concepts))
panels = []
for i, c in enumerate(concepts):
    n, slug = c['slug'][:2], c['slug']
    panels.append(f'''<section id="panel-{n}" role="tabpanel" aria-labelledby="tab-{n}" tabindex="0"{"" if i == 0 else " hidden"}>
<div class="section-title"><h2>{n} / {c['name']}</h2><a href="{prefix}svg/{slug}.svg" download>Скачать SVG ↓</a></div>
<a href="{prefix}applications/{slug}-board.png" target="_blank"><img src="{prefix}applications/{slug}-board.png" alt="{c['ru']}: сайт и Instagram" width="1600" height="1200"></a>
<div class="links"><a href="{prefix}svg-dark/{slug}.svg" download>SVG для тёмного фона ↓</a><a href="{prefix}applications/{slug}-website.png" target="_blank">Сайт отдельно ↗</a><a href="{prefix}applications/{slug}-instagram.png" target="_blank">Instagram отдельно ↗</a><a href="{prefix}applications/{slug}.html" target="_blank">Макет HTML ↗</a></div></section>''')

for filename in ['index.html', 'applications.html']:
    target = ROOT / filename
    before = target.read_text()
    if marker in before:
        print(filename + ': already integrated')
        continue
    assert 'id="tab-31"' in before and 'id="tab-21"' not in before
    after = before.replace('<nav role="tablist" aria-label="Выбрать новый вариант">',
                           '<nav role="tablist" aria-label="Выбрать новый вариант">' + marker + tabs, 1)
    # 31 was the default selection; 21 now comes first in numeric order.
    after = after.replace('id="tab-31" role="tab" aria-controls="panel-31" aria-selected="true" tabindex="0"',
                          'id="tab-31" role="tab" aria-controls="panel-31" aria-selected="false" tabindex="-1"', 1)
    after = after.replace('<section id="panel-31" role="tabpanel" aria-labelledby="tab-31" tabindex="0">',
                          marker + '\n'.join(panels) + '\n<section id="panel-31" role="tabpanel" aria-labelledby="tab-31" tabindex="0" hidden>', 1)
    after = after.replace('<title>Tatsi in motion — 10 новых вариантов по референсу</title>',
                          '<title>Tatsi in motion — 20 вариантов по референсу</title>', 1)
    after = after.replace('10 новых вариантов по вашему референсу — 31–40. Каллиграфические t, антиквенные T, открытые орбиты и мятные ленты.',
                          '20 вариантов по вашему референсу: 21–30 (буквы из антиквы и каллиграфии, рисованы для белого фона) и 31–40 (рисованные контуры). '
                          'Каллиграфические t, антиквенные T, открытые орбиты и мятные ленты.', 1)
    after = after.replace('Скачать 10 SVG и все макеты ↓', 'Скачать 31–40: SVG и макеты ↓', 1)
    assert after != before
    target.write_text(after)
    print(filename + ': added 21-30 in front of 31-40')
