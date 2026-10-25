"""Build contextual boards and a single-panel hover gallery for all refinements."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent/'logo-concepts-2026-10-25'
concepts=json.loads((ROOT/'concepts.json').read_text())
bounds={r['code']:r['bounds'] for r in json.loads((ROOT/'vector-verification.json').read_text())['files']}
template=(OLD/'applications/01-flowing-t.html').read_text()
assert len(re.findall(r'<svg\b.*?</svg>',template,re.S))==6

def symbol(c,instance):
    svg=(ROOT/'svg'/f"{c['slug']}.svg").read_text()
    svg=re.sub(r'<\?xml[^>]*>\s*','',svg)
    b=bounds[c['code']]
    viewbox=f"{b['x']-24:.3f} {b['y']-24:.3f} {b['width']+48:.3f} {b['height']+48:.3f}"
    svg=re.sub(r'viewBox="[^"]+"',f'viewBox="{viewbox}"',svg)
    prefix=f"{c['slug']}-{instance}-"
    svg=re.sub(r'\bid="([^"]+)"',lambda m:f'id="{prefix}{m[1]}"',svg)
    return re.sub(r'aria-labelledby="([^"]+)"',lambda m:'aria-labelledby="'+' '.join(prefix+x for x in m[1].split())+'"',svg)

for c in concepts:
    instances=iter(['hero','site','avatar','post','photo','mini'])
    board=re.sub(r'<svg\b.*?</svg>',lambda _:symbol(c,next(instances)),template,flags=re.S)
    board=board.replace('01 · Flowing T',f"{c['code']} · {c['name']}")
    board=board.replace('Tatsi in motion / 01 of 10',f"Tatsi in motion / refinements / {c['code']}")
    board=board.replace('<h1>Flowing T</h1>',f"<h1>{c['code']} · {c['name']}</h1>")
    board=re.sub(r'<p class="concept-note">.*?</p>',f'<p class="concept-note">{html.escape(c["idea"])}</p>',board)
    board=board.replace('Вариант 01 · Пластичная T',f"Вариант {c['code']} · {c['name']}")
    if c['letter_style'] in ['fine','italic','loop','script']:
        font='font-family:Georgia,serif;font-weight:400;'+('font-style:italic;' if c['letter_style'] in ['italic','loop'] else '')
    else:
        font='font-family:Arial,sans-serif;font-weight:'+('600;' if c['letter_style']=='bold' else '400;')
    board=board.replace('</style>',f'.site-brand>span{{{font}}}.board-heading h1{{font-size:30px}}</style>')
    (ROOT/'applications'/f"{c['slug']}.html").write_text(board)

css='''*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#0c1717;color:#f5faf8;font:16px/1.5 Arial,sans-serif}main{max-width:1500px;margin:auto;padding:34px 32px 60px}a{color:#bcf7f3;text-underline-offset:4px}header .eyebrow{font-size:11px;letter-spacing:.14em;color:#a5bdb5;text-transform:uppercase}h1{font-size:clamp(28px,4vw,48px);line-height:1.15;font-weight:500;margin:16px 0}header p{max-width:820px;color:#b3c6c0}.downloads{display:flex;gap:20px;flex-wrap:wrap;align-items:center;margin:22px 0}.download{background:#bcf7f3;color:#142627;text-decoration:none;padding:12px 18px;border-radius:4px}nav{position:sticky;top:0;z-index:2;background:#0c1717f5;backdrop-filter:blur(12px);border-block:1px solid #34514b;margin:28px 0;padding:15px 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}.group-label{font-size:12px;color:#aec5be;margin:0 0 9px}.tab-row{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px}[role=tab]{display:block;text-align:center;padding:8px 2px;border:1px solid #3b5a51;border-radius:3px;text-decoration:none;font-size:14px;transition:background .12s,color .12s}[role=tab][aria-selected=true]{background:#bcf7f3;color:#142627;border-color:#bcf7f3}a:focus-visible{outline:2px solid #bcf7f3;outline-offset:4px}[hidden]{display:none!important}.selected-top{display:grid;grid-template-columns:260px minmax(0,1fr);gap:34px;align-items:center;margin:20px 0 30px}.large-mark{display:block;width:260px;height:260px;background:#142627;border-radius:8px}.details h2{font-size:30px;font-weight:500;line-height:1.2;margin:0 0 12px}.details>p{color:#b3c6c0;max-width:650px}.swatches{display:flex;gap:10px;align-items:center;margin:18px 0}.swatches img{width:72px;height:72px;border-radius:3px}.swatches .white{background:#fff}.swatches .dark{background:#142627}.swatches span{font-size:12px;max-width:240px;color:#a9c3b9}.links{display:flex;gap:16px;flex-wrap:wrap;font-size:13px}.board{display:block;width:100%;height:auto;border-radius:8px}.application-label{font-size:13px;color:#abc2ba;margin:22px 0 10px}footer{border-top:1px solid #34514b;margin-top:40px;padding-top:20px;color:#a7bdb5;font-size:13px}footer p{max-width:900px}@media(max-width:900px){nav{grid-template-columns:1fr;gap:10px;padding:10px 0}.selector-group{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:10px}.group-label{margin:0}main{padding:24px 20px 40px}.selected-top{grid-template-columns:180px 1fr;gap:20px}.large-mark{width:180px;height:180px}.details h2{font-size:25px}}@media(max-width:540px){main{padding:20px 14px 32px}.selector-group{display:block}.group-label{font-size:10px;margin:0 0 4px}.tab-row{gap:5px}[role=tab]{padding:5px 1px;font-size:13px}nav{gap:7px}.selected-top{display:block}.large-mark{width:100%;height:auto;max-height:330px}.details{margin-top:20px}.details h2{font-size:27px}.downloads{gap:12px;font-size:14px}.links{gap:12px}header p{font-size:14px}}@media(prefers-reduced-motion:reduce){*{transition:none!important}}'''
labels={'A':'A · Мятная t и нижняя волна','B':'B · Белая t в открытой орбите','C':'C · Кистевая T'}
selectors=[]
panels=[]
for group,label in labels.items():
    tabs=''.join(f'<a href="#concept-{c["code"]}" id="tab-{c["code"]}" role="tab" aria-controls="panel-{c["code"]}" aria-selected="{str(c["code"]=="A1").lower()}" tabindex="{0 if c["code"]=="A1" else -1}">{c["code"]}</a>' for c in concepts if c['group']==group)
    selectors.append(f'<div class="selector-group"><p class="group-label">{label}</p><div class="tab-row">{tabs}</div></div>')
for c in concepts:
    code,slug=c['code'],c['slug']
    hidden='' if code=='A1' else ' hidden'
    panels.append(f'''<section id="panel-{code}" role="tabpanel" aria-labelledby="tab-{code}"{hidden}>
<div class="selected-top"><img class="large-mark" src="svg/{slug}.svg" width="512" height="512" alt="{code} — {c['name']}"><div class="details"><h2>{code} / {c['name']}</h2><p>{c['idea']}</p>
<div class="swatches"><img class="white" src="svg-light/{slug}.svg" alt="Версия для белого фона"><img class="dark" src="svg/{slug}.svg" alt="Основная версия"><span>На белом и тёмном фоне.<br>Мятный цвет: #bcf7f3</span></div><div class="links"><a href="svg/{slug}.svg" download>Скачать SVG ↓</a><a href="svg-light/{slug}.svg" download>SVG для светлого фона ↓</a><a href="png/{slug}.png" download>PNG 1024 px ↓</a></div></div></div>
<p class="application-label">Этот вариант на сайте и в Instagram</p><a href="applications/{slug}-board.png" target="_blank"><img class="board" src="applications/{slug}-board.png" alt="{code}: примеры сайта и Instagram" width="1600" height="1200"></a>
<div class="links" style="margin-top:16px"><a href="applications/{slug}-website.png" target="_blank">Сайт отдельно ↗</a><a href="applications/{slug}-instagram.png" target="_blank">Instagram отдельно ↗</a><a href="applications/{slug}.html" target="_blank">Макет HTML ↗</a></div></section>''')
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tatsi in motion — 3 направления × 7 вариантов</title><style>{css}</style></head><body><main><header><p class="eyebrow">Tatsi in motion / refinement collection</p><h1>Три любимых направления.<br>По семь новых вариантов.</h1><p>Наведите мышь на A1–C7 — ниже появится один выбранный логотип и его примерка на сайте и в Instagram. На телефоне нажмите на номер.</p><div class="downloads"><a class="download" href="tatsi-refinements-21.zip" download>Скачать 21 вариант и все макеты ↓</a><a href="preview/overview.png" target="_blank">Сравнить все 21 ↗</a></div></header><nav role="tablist" aria-label="21 вариант по трём выбранным направлениям">{''.join(selectors)}</nav>{''.join(panels)}<footer><p>SVG — исходник для редактирования. PNG — экспорт для просмотра. В SVG нет встроенных картинок и зависимостей от шрифтов. В C5 фактура кисти выполнена векторными контурами.</p><p>Основной цвет #bcf7f3 очень светлый: на белом он выглядит мягче, особенно в тонких вариантах. Примеры профиля Instagram условные, публикации служат для сравнения оформления.</p></footer></main><script src="applications.js"></script></body></html>'''
(ROOT/'applications.html').write_text(page)
(ROOT/'index.html').write_text(page)
(ROOT/'applications.js').write_text((OLD/'applications.js').read_text())
print('Built 21 boards and one gallery with 3 groups of 7 hover selectors.')
