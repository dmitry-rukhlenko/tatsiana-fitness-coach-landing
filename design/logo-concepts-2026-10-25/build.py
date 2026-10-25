"""Build ten original vector concepts and their local comparison gallery."""

from pathlib import Path
from html import escape
import json
import zipfile

ROOT = Path(__file__).resolve().parent
WHITE = "#ffffff"
MINT = "#bcf7f3"


def stroke(name, d, color=WHITE, width=22):
    return f'<path id="{name}" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def fill(name, d, color=WHITE):
    return f'<path id="{name}" d="{d}" fill="{color}"/>'


def circle(name, x, y, r, color=MINT):
    return f'<circle id="{name}" cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


# Every design has independently editable paths. No font or bitmap is embedded.
concepts = [
    {
        "slug": "01-flowing-t", "name": "Flowing T", "ru": "Пластичная T",
        "idea": "Наклонная t с мягким изгибом: устойчивость и свобода движения в одном жесте.",
        "type": "Буква · пластика",
        "body": [
            stroke("t-stem", "M281 128 L237 320 C226 367 254 392 309 363", width=28),
            stroke("flowing-crossbar", "M145 211 C206 189 283 191 366 207", MINT, 24),
        ],
    },
    {
        "slug": "02-open-reach", "name": "Open Reach", "ru": "Свободный жест",
        "idea": "Раскрытая фигура без спортивной агрессии. Акцент на подвижности и ощущении своего тела.",
        "type": "Фигура · открытость",
        "body": [
            circle("head", 287, 133, 19),
            stroke("open-arms", "M137 193 C209 235 278 225 359 161", width=23),
            stroke("body-and-grounded-leg", "M260 220 C247 275 216 333 170 376", width=25),
            stroke("moving-leg", "M239 282 C284 305 305 344 338 371", MINT, 23),
        ],
    },
    {
        "slug": "03-tm-ligature", "name": "TM Ligature", "ru": "Инициалы TM",
        "idea": "Точная монограмма с общим наклоном. Прямая T отвечает за силу, раскрытая M — за движение.",
        "type": "Монограмма · сила",
        "body": [
            stroke("t-top", "M125 166 H290", width=25),
            stroke("t-stem", "M213 166 L165 351", width=25),
            stroke("m", "M234 351 L277 188 L302 279 L378 188 L335 351", MINT, 22),
        ],
    },
    {
        "slug": "04-orbit-t", "name": "Orbit T", "ru": "Орбита движения",
        "idea": "Разомкнутая орбита окружает t. Продолжение траектории остаётся открытым.",
        "type": "Буква · траектория",
        "body": [
            stroke("open-orbit", "M384 238 C400 159 346 109 270 119 C184 130 119 202 125 278 C131 358 199 400 276 382 C308 374 334 359 355 336", width=20),
            stroke("t-stem", "M283 184 L253 310 C246 339 264 346 288 332", MINT, 20),
            stroke("t-crossbar", "M205 239 Q261 226 317 235", MINT, 19),
        ],
    },
    {
        "slug": "05-elastic-m", "name": "Elastic M", "ru": "Упругая M",
        "idea": "Непрерывная упругая линия складывается в m: движение без жёстких углов и остановок.",
        "type": "Буква · непрерывность",
        "body": [
            stroke("elastic-m", "M122 336 L154 209 C164 164 218 170 218 213 L218 292 L274 212 C304 170 342 182 332 226 L313 303 C304 341 340 354 380 318", width=27),
            stroke("moving-tip", "M342 343 C354 341 368 332 380 318", MINT, 27),
        ],
    },
    {
        "slug": "06-tatsi-wordmark", "name": "Tatsi", "ru": "Личное имя",
        "idea": "Авторское округлое написание tatsi. Две t задают ритм, мятная точка добавляет лёгкость.",
        "type": "Написание · личный бренд",
        "body": [
            '<g id="custom-wordmark" transform="translate(23 115) scale(.91)">',
            stroke("first-t", "M59 88 V229 Q59 254 84 247 M31 145 H89", width=13),
            stroke("a-bowl", "M191 191 C191 129 115 128 115 193 C115 251 191 252 191 191", width=13),
            stroke("a-stem", "M191 149 V244", width=13),
            stroke("second-t", "M237 88 V229 Q237 254 262 247 M210 145 H268", width=13),
            stroke("s", "M351 154 C332 136 294 140 294 166 C294 195 353 185 353 218 C353 246 315 256 291 235", width=13),
            stroke("i", "M395 151 V244", width=13),
            circle("i-dot", 395, 111, 10),
            stroke("motion-after-i", "M420 108 L449 93", MINT, 8),
            '</g>',
        ],
    },
    {
        "slug": "07-free-stride", "name": "Free Stride", "ru": "Свободный шаг",
        "idea": "Две широкие пластичные формы напоминают шаг и разворот корпуса. Сильный силуэт для одежды.",
        "type": "Силуэт · энергия",
        "body": [
            circle("head", 295, 132, 21),
            fill("upper-body", "M129 193 C194 207 256 197 347 166 C333 193 310 211 283 225 C259 244 241 270 220 309 C206 334 181 356 147 369 C183 327 200 287 219 241 C183 237 153 219 129 193 Z"),
            fill("extended-leg", "M249 269 C287 272 311 297 325 322 C340 347 356 363 379 376 C340 376 313 359 294 337 C275 313 256 299 230 297 Z", MINT),
        ],
    },
    {
        "slug": "08-pivot-t", "name": "Pivot T", "ru": "Точка опоры",
        "idea": "Геометричная T с отделённой перекладиной. Наклон задаёт движение, широкие формы — уверенность.",
        "type": "Геометрия · устойчивость",
        "body": [
            '<g id="pivot-symbol" transform="rotate(-12 256 256)">',
            fill("crossbar", "M139 143 H373 Q387 143 387 157 V184 Q387 198 373 198 H139 Q125 198 125 184 V157 Q125 143 139 143 Z", MINT),
            fill("stem", "M227 219 H285 V310 C285 342 301 353 329 342 L337 380 C282 401 227 378 227 322 Z"),
            '</g>',
        ],
    },
    {
        "slug": "09-in-motion", "name": "In motion", "ru": "В движении",
        "idea": "Компактное написание motion с раскрытой o. Разрыв в букве превращает слово в траекторию.",
        "type": "Написание · движение",
        "body": [
            '<g id="custom-wordmark" transform="translate(46 204) scale(.84)">',
            stroke("m", "M10 105 V27 M10 52 C10 9 65 9 65 49 V105 M65 52 C65 9 120 9 120 49 V105", width=11),
            stroke("first-o", "M206 88 C187 126 141 108 141 67 C141 19 202 12 210 53", width=11),
            stroke("o-moving-end", "M210 53 Q212 64 209 73", MINT, 11),
            stroke("t", "M245 -2 V86 Q245 108 266 102 M228 30 H271", width=11),
            stroke("i", "M296 32 V105", width=11),
            circle("i-dot", 296, 4, 8),
            stroke("second-o", "M391 67 C391 13 325 13 325 67 C325 121 391 121 391 67", width=11),
            stroke("n", "M416 105 V29 M416 54 C416 10 475 10 475 52 V105", width=11),
            '</g>',
        ],
    },
    {
        "slug": "10-tm-ribbon", "name": "TM Ribbon", "ru": "Лента TM",
        "idea": "Мягкая монограмма tm одним росчерком. Петелька t и два подъёма m соединяют личность и движение.",
        "type": "Монограмма · плавность",
        "body": [
            stroke("ribbon-tm", "M112 237 C165 231 207 206 216 167 C225 125 189 127 179 172 L151 298 C141 345 169 365 196 324 L243 249 C260 219 284 225 275 263 L259 326 L307 253 C328 221 350 230 339 268 L328 308 C319 343 342 351 377 323", width=18),
            stroke("t-crossbar", "M121 238 C166 236 208 231 247 223", MINT, 16),
        ],
    },
]


def master(c):
    title = f'Tatsi in motion — {c["name"]}'
    return '\n'.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-labelledby="logo-title logo-description">',
        f'  <title id="logo-title">{escape(title)}</title>',
        f'  <desc id="logo-description">{escape(c["idea"])} Transparent background; editable vector shapes; white #ffffff and mint #bcf7f3.</desc>',
        f'  <g id="{c["slug"]}-artwork">',
        *['    ' + part for part in c['body']],
        '  </g>',
        '</svg>',
        '',
    ])


for c in concepts:
    (ROOT / 'svg' / f'{c["slug"]}.svg').write_text(master(c))

(ROOT / 'concepts.json').write_text(json.dumps(
    [{k: v for k, v in c.items() if k != 'body'} for c in concepts],
    ensure_ascii=False, indent=2) + '\n')

cards = []
for i, c in enumerate(concepts, 1):
    cards.append(f'''<article class="concept" id="concept-{i:02d}">
      <div class="card-top"><span class="number">{i:02d}</span><span>{c['type']}</span></div>
      <div class="art"><img src="svg/{c['slug']}.svg" alt="{escape(c['ru'])}" width="512" height="512"></div>
      <div class="card-bottom"><div><h2>{c['name']}</h2><p class="ru">{c['ru']}</p></div><a href="svg/{c['slug']}.svg" download aria-label="Скачать {escape(c['name'])} в SVG">SVG <span aria-hidden="true">↓</span></a></div>
      <p class="rationale">{c['idea']}</p>
    </article>''')

gallery = '''<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tatsi in motion — 10 logo concepts</title>
<style>
*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#0b1516;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:inherit}main{max-width:1440px;margin:auto;padding:60px 48px 36px}header{display:flex;justify-content:space-between;gap:28px;align-items:flex-end;padding-bottom:36px;border-bottom:1px solid #304142;margin-bottom:28px}.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#bcf7f3;margin:0 0 14px}h1{font-size:clamp(32px,4vw,56px);font-weight:450;letter-spacing:-.035em;margin:0 0 12px}.intro{color:#b9c6c5;max-width:650px;line-height:1.5;font-size:15px;margin:0}.palette{display:flex;gap:22px;margin-bottom:22px;font-size:12px;color:#b9c6c5}.swatch{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px}.download-all{font-size:14px;display:inline-block;border:1px solid #536867;border-radius:4px;padding:12px 16px;text-decoration:none;white-space:nowrap}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.concept{background:#142627;padding:20px 22px 22px;min-width:0}.card-top{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:10px;color:#93aaa7;letter-spacing:.06em}.number{color:#bcf7f3;font-size:14px;font-variant-numeric:tabular-nums}.art{height:260px;display:flex;align-items:center;justify-content:center}.art img{height:100%;width:100%;object-fit:contain}.card-bottom{display:flex;justify-content:space-between;gap:12px;align-items:center}h2{font-size:20px;font-weight:500;letter-spacing:-.02em;margin:0 0 5px}.ru{font-size:12px;color:#a3b7b3;margin:0}.card-bottom a{font-size:11px;letter-spacing:.05em;text-decoration:none;color:#bcf7f3;border:1px solid #415b57;border-radius:3px;padding:8px 10px}.card-bottom a:hover,.download-all:hover{background:#24403d}.rationale{margin:20px 0 0;color:#a3b7b3;font-size:13px;line-height:1.55;min-height:60px}footer{display:flex;justify-content:space-between;gap:20px;color:#8fa5a2;font-size:12px;line-height:1.6;border-top:1px solid #304142;margin-top:32px;padding-top:22px}a:focus-visible{outline:2px solid #bcf7f3;outline-offset:4px}@media(min-width:1250px){.grid{grid-template-columns:repeat(5,minmax(0,1fr))}.concept{padding:16px}.art{height:225px}.card-top{font-size:8px}.rationale{font-size:11px;min-height:90px}h2{font-size:17px}.card-bottom a{padding:6px}.card-bottom{gap:6px}.ru{font-size:10px}}@media(max-width:850px){main{padding:36px 24px}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}header{display:block}.actions{margin-top:24px}.palette{margin-bottom:16px}.art{height:240px}}@media(max-width:520px){main{padding:28px 18px}.grid{grid-template-columns:1fr}.art{height:280px}.rationale{min-height:0}footer{display:block}footer p{margin-top:0}}
</style></head><body><main>
<header><div><p class="eyebrow">Logo exploration / 01—10</p><h1>Tatsi in motion.</h1><p class="intro">Сила, подвижность и свобода в своём теле.<br>Десять разных знаков для выбора направления.</p></div><div class="actions"><div class="palette"><span><i class="swatch" style="background:#fff"></i>#ffffff</span><span><i class="swatch" style="background:#bcf7f3"></i>#bcf7f3</span></div><a class="download-all" href="tatsi-in-motion-10-svg.zip" download>Скачать 10 SVG ↓</a></div></header>
<section class="grid" aria-label="Десять вариантов логотипа">CARDS</section>
<footer><p>Каждый знак — отдельный редактируемый SVG без шрифтов и растровых изображений.<br>Тёмный фон нужен только для просмотра. Фон файлов прозрачный.</p><p>25.10.2026<br>Концепции для выбора</p></footer>
</main></body></html>'''.replace('CARDS', '\n'.join(cards))
(ROOT / 'index.html').write_text(gallery)

# The contact sheet is a presentation artifact, not another logo candidate.
sheet = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1060" viewBox="0 0 1600 1060">',
    '<rect width="1600" height="1060" fill="#0b1516"/>',
    '<g font-family="Arial, Helvetica, sans-serif">',
    '<text x="58" y="57" font-size="13" letter-spacing="3" fill="#bcf7f3">LOGO EXPLORATION / 01—10</text>',
    '<text x="55" y="123" font-size="52" font-weight="400" fill="#ffffff">Tatsi in motion.</text>',
    '<text x="58" y="164" font-size="17" fill="#a3b7b3">Strength. Mobility. Freedom to move.</text>',
    '<circle cx="1280" cy="110" r="7" fill="#ffffff"/><text x="1296" y="116" font-size="14" fill="#a3b7b3">#ffffff</text>',
    '<circle cx="1410" cy="110" r="7" fill="#bcf7f3"/><text x="1426" y="116" font-size="14" fill="#a3b7b3">#bcf7f3</text>',
]
for i, c in enumerate(concepts):
    x = 56 + (i % 5) * 302
    y = 214 + (i // 5) * 376
    sheet.extend([
        f'<rect x="{x}" y="{y}" width="280" height="354" rx="2" fill="#142627"/>',
        f'<text x="{x + 20}" y="{y + 31}" font-size="13" fill="#bcf7f3">{i + 1:02d}</text>',
        f'<g transform="translate({x + 4} {y + 21}) scale(.53125)">',
        *[part.replace('id="', f'id="sheet-{i}-') for part in c['body']],
        '</g>',
        f'<text x="{x + 20}" y="{y + 316}" font-size="19" fill="#ffffff">{c["name"]}</text>',
        f'<text x="{x + 20}" y="{y + 338}" font-size="11" fill="#a3b7b3">{escape(c["type"])}</text>',
    ])
sheet.extend([
    '<text x="58" y="1017" font-size="14" fill="#a3b7b3">10 отдельных SVG · прозрачный фон · редактируемые контуры</text>',
    '<text x="1540" y="1017" font-size="13" text-anchor="end" fill="#a3b7b3">25.10.2026 / CONCEPTS</text>',
    '</g></svg>',
])
(ROOT / 'preview' / 'contact-sheet.svg').write_text('\n'.join(sheet))

with zipfile.ZipFile(ROOT / 'tatsi-in-motion-10-svg.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted((ROOT / 'svg').glob('*.svg')):
        archive.write(path, f'tatsi-in-motion/{path.name}')

print(f'Created {len(concepts)} SVG masters, comparison sheet, local gallery and ZIP.')
