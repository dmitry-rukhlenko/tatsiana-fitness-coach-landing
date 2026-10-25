"""Keep A2 intact and compare three small, separately editable flourishes."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'logo-refinements-2026-10-25'
for name in ['svg','png','applications','preview']:(ROOT/name).mkdir(exist_ok=True)
source=(PREVIOUS/'svg/a2.svg').read_text()
concepts=[
 dict(code='A2',slug='a2',name='Без добавления',idea='Исходный тонкий знак — для сравнения.',curl=None),
 dict(code='D1',slug='d1',name='Петля на волне',idea='Небольшой завиток продолжает правый конец перекладины. Один лёгкий акцент.',curl='M410 203 C431 194 441 181 432 175 C425 170 414 179 421 184 C425 188 430 186 430 182'),
 dict(code='D2',slug='d2',name='Росчерк у буквы',idea='Тонкий завиток завершает ножку t и делает знак похожим на личную подпись.',curl='M290 351 C306 337 322 330 322 342 C322 350 310 353 307 346 C304 340 310 335 314 339'),
 dict(code='D3',slug='d3',name='Завиток внизу',idea='Маленькая петля встроена в начало нижней волны. Верхняя часть остаётся спокойной.',curl='M225 403 C208 402 197 412 205 420 C213 428 226 420 220 414 C216 410 210 413 212 417'),
]
template=(PREVIOUS/'applications/a2.html').read_text()
for c in concepts:
    svg=source
    if c['curl']:
        new_path=f'<path id="small-flourish" d="{c["curl"]}" fill="none" stroke="#bcf7f3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        assert svg.endswith('</g></svg>\n')
        svg=svg.removesuffix('</g></svg>\n')+new_path+'</g></svg>\n'
        svg=re.sub(r'<title[^>]*>.*?</title>',f'<title id="title">Tatsi in motion — {c["code"]} · {c["name"]}</title>',svg)
        svg=re.sub(r'<desc[^>]*>.*?</desc>',f'<desc id="desc">{c["idea"]} Editable vector; original A2 contours preserved.</desc>',svg)
    (ROOT/'svg'/f'{c["slug"]}.svg').write_text(svg)
    def instance(m):
        prefix=f'{c["slug"]}-{next(instances)}-'
        mark=re.sub(r'<\?xml[^>]*>\s*','',svg)
        mark=mark.replace('viewBox="0 0 512 512"','viewBox="45.44 41.97 418.63 428.33"')
        mark=re.sub(r'\bid="([^"]+)"',lambda m:f'id="{prefix}{m[1]}"',mark)
        return re.sub(r'aria-labelledby="([^"]+)"',lambda m:'aria-labelledby="'+' '.join(prefix+x for x in m[1].split())+'"',mark)
    instances=iter(['hero','site','avatar','post','photo','mini'])
    board=re.sub(r'<svg\b.*?</svg>',instance,template,flags=re.S)
    board=board.replace('A2 · Тонкое перо',f'{c["code"]} · {c["name"]}').replace('refinements / A2',f'A2 details / {c["code"]}')
    board=re.sub(r'<p class="concept-note">.*?</p>',f'<p class="concept-note">{c["idea"]}</p>',board)
    (ROOT/'applications'/f'{c["slug"]}.html').write_text(board)

(ROOT/'concepts.json').write_text(json.dumps(concepts,ensure_ascii=False,indent=2)+'\n')
(ROOT/'source-baseline.json').write_text(json.dumps({'source':'../logo-refinements-2026-10-25/svg/a2.svg','sha256':hashlib.sha256(source.encode()).hexdigest()},indent=2)+'\n')
cards=''.join(f'''<article><p class="code">{c['code']} · {c['name']}</p><div class="art"><img src="../svg/{c['slug']}.svg" alt="{c['name']}"></div><p class="note">{c['idea']}</p><div class="size"><img src="../svg/{c['slug']}.svg" width="64" height="64" alt="Малый размер"><span>Проверка в небольшом размере</span></div></article>''' for c in concepts)
sheet=f'''<!doctype html><html lang="ru"><meta charset="utf-8"><style>*{{box-sizing:border-box}}body{{margin:0;background:#eff2ee;color:#142627;font:15px/1.45 Arial,sans-serif}}main{{padding:36px}}h1{{font-size:34px;font-weight:500;margin:8px 0}}header p{{margin:0 0 26px;color:#4b6861}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}article{{background:white}}.code{{padding:16px 16px 0;margin:0;font-size:15px}}.art{{margin:14px 0 0;background:#142627}}.art img{{width:100%;display:block}}.note{{padding:0 16px;min-height:66px;font-size:13px;color:#4b6861}}.size{{margin:0 16px 16px;display:flex;gap:12px;align-items:center;font-size:11px;color:#4b6861}}.size img{{background:#142627;border-radius:50%}}</style><main><header><h1>A2: три маленьких росчерка.</h1><p>Исходный вариант и три дополнения · один новый акцент в каждом знаке</p></header><div class="grid">{cards}</div></main></html>'''
(ROOT/'preview/comparison.html').write_text(sheet)
css='''*{box-sizing:border-box}body{margin:0;background:#0c1717;color:#f5faf8;font:16px/1.5 Arial,sans-serif}main{max-width:1450px;margin:auto;padding:32px}h1{font-size:clamp(28px,4vw,44px);font-weight:500;margin:12px 0}p{color:#b3c6c0}a{color:#bcf7f3;text-underline-offset:4px}nav{position:sticky;top:0;background:#0c1717;padding:16px 0;display:flex;gap:10px;flex-wrap:wrap;border-block:1px solid #34514b;margin:24px 0}nav a{padding:8px 16px;border:1px solid #34514b;text-decoration:none;border-radius:4px}nav a[aria-selected=true]{background:#bcf7f3;color:#142627}a:focus-visible{outline:2px solid #bcf7f3;outline-offset:3px}[hidden]{display:none!important}.top{display:grid;grid-template-columns:280px 1fr;gap:30px;align-items:center;margin:24px 0}.mark{width:280px;height:280px;background:#142627;border-radius:6px}h2{font-size:28px;font-weight:500;margin:0}section .board{width:100%;display:block;border-radius:6px}.links{display:flex;gap:18px;flex-wrap:wrap;font-size:14px;margin:16px 0}.comparison{width:100%;display:block;margin-top:40px}footer{margin-top:32px;border-top:1px solid #34514b;font-size:13px}@media(max-width:600px){main{padding:20px 14px}.top{display:block}.mark{width:100%;height:auto}.top>div{margin-top:20px}nav{gap:7px}nav a{padding:7px 12px}h2{font-size:24px}}'''
tabs=''.join(f'<a role="tab" id="tab-{c["code"]}" aria-controls="panel-{c["code"]}" aria-selected="{str(c["code"]=="D1").lower()}" tabindex="{0 if c["code"]=="D1" else -1}" href="#concept-{c["code"]}">{c["code"]}</a>' for c in concepts)
panels=[]
for c in concepts:
    hidden='' if c['code']=='D1' else ' hidden'
    panels.append(f'''<section role="tabpanel" id="panel-{c['code']}" aria-labelledby="tab-{c['code']}"{hidden}><div class="top"><img class="mark" src="svg/{c['slug']}.svg" alt="{c['name']}"><div><h2>{c['code']} / {c['name']}</h2><p>{c['idea']}</p><div class="links"><a href="svg/{c['slug']}.svg" download>SVG ↓</a><a href="png/{c['slug']}.png" download>PNG 1024 px ↓</a></div></div></div><a href="applications/{c['slug']}-board.png" target="_blank"><img class="board" src="applications/{c['slug']}-board.png" width="1600" height="1200" alt="{c['code']}: сайт и Instagram"></a><div class="links"><a href="applications/{c['slug']}-website.png" target="_blank">Сайт отдельно ↗</a><a href="applications/{c['slug']}-instagram.png" target="_blank">Instagram отдельно ↗</a></div></section>''')
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tatsi in motion — маленький росчерк для A2</title><style>{css}</style></head><body><main><h1>Маленький росчерк для A2.</h1><p>Три версии с одним новым акцентом. Наведите мышь на номер, чтобы сравнить; на телефоне нажмите.</p><div class="links"><a href="tatsi-a2-flourishes.zip" download>Скачать SVG, PNG и макеты ↓</a><a href="preview/comparison.png" target="_blank">Сравнить все четыре ↗</a></div><nav role="tablist" aria-label="A2 и три небольших дополнения">{tabs}</nav>{''.join(panels)}<footer><p>Исходный A2 сохранён. Цвет #bcf7f3. Завитушка — отдельный редактируемый векторный контур; её толщину можно изменить независимо.</p></footer></main><script src="applications.js"></script></body></html>'''
(ROOT/'applications.html').write_text(page)
script=(PREVIOUS/'applications.js').read_text().replace('|| tabs[0], false','|| tabs[1], false')
(ROOT/'applications.js').write_text(script)
print('Built A2 comparison and three editable flourishes: D1, D2, D3.')
