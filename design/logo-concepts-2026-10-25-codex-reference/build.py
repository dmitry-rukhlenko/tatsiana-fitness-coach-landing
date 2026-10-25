"""Create the ten reference-led, font-independent vector concepts."""

from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
WHITE, MINT, INK = '#ffffff', '#bcf7f3', '#142627'


def shape(name, d, color=MINT):
    return f'<path id="{name}" d="{d}" fill="{color}"/>'


def line(name, d, color=MINT, width=4):
    return f'<path id="{name}" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


# Tapered strokes are closed Bezier contours, rather than raster traces.
SCRIPT_T = 'M303 137 C311 126 322 132 314 146 C282 193 249 253 228 305 C212 344 211 374 239 374 C261 373 284 354 305 330 C286 370 254 394 228 390 C190 386 194 350 210 311 C235 247 271 185 303 137 Z'
HALO = 'M409 163 C373 105 311 75 246 80 C149 87 79 165 83 259 C87 357 162 429 256 429 C351 429 425 357 433 266 C438 365 361 442 258 442 C153 442 72 365 69 260 C65 158 144 75 246 69 C314 65 375 100 409 163 Z'
SWELL = 'M124 221 C171 173 230 181 291 195 C342 207 385 206 419 184 C389 215 346 221 292 207 C230 192 175 184 124 221 Z'
SERIF_T = 'M132 125 H379 L383 182 H375 C363 145 344 138 284 138 V355 C284 381 292 392 321 397 V404 H191 V397 C220 392 228 381 228 355 V138 C169 138 148 146 137 182 H129 Z'

concepts = [
    dict(slug='31-halo-script', name='Halo Script', ru='Каллиграфия в орбите',
         idea='Лёгкая открытая окружность и наклонная t. Волна становится перекладиной буквы.',
         type='Орбита · каллиграфия', body=[shape('open-halo', HALO), shape('t', SCRIPT_T, WHITE), shape('wave-crossbar', SWELL)]),
    dict(slug='32-ribbon-serif', name='Ribbon Serif', ru='Лента и антиква',
         idea='Выразительная T с тонкими засечками. Мятная лента проходит сквозь вертикаль и поднимается вправо.',
         type='Антиква · лента', body=[
             shape('upper-t', 'M128 120 H381 L385 177 H377 C366 141 346 133 284 133 V224 C264 233 245 244 228 257 V133 C166 133 146 143 135 177 H127 Z', WHITE),
             shape('lower-t', 'M228 287 C244 271 264 261 284 254 V354 C284 382 294 393 321 398 V405 H191 V398 C219 393 228 382 228 354 Z', WHITE),
             shape('rising-ribbon', 'M72 204 C144 248 211 256 266 225 C331 188 393 193 443 145 C408 204 353 212 285 240 C213 269 146 263 72 204 Z'),
         ]),
    dict(slug='33-air-signature', name='Air Signature', ru='Воздушная подпись',
         idea='Размашистая заглавная T с открытой петлёй. Смена толщины штриха напоминает движение пера.',
         type='Подпись · росчерк', body=[
             shape('calligraphic-stem', 'M332 131 C307 174 276 231 248 287 C222 341 207 385 177 399 C160 407 139 401 141 382 C143 362 171 349 197 345 C174 352 153 368 153 382 C153 394 167 397 177 390 C202 372 217 319 236 272 C257 221 285 164 307 135 Z', WHITE),
             shape('looped-cap', 'M99 220 C54 185 98 122 171 117 C250 110 285 152 342 153 C385 153 413 133 410 110 C407 88 369 88 344 112 C327 128 316 147 311 161 C315 132 331 110 349 98 C382 75 420 84 420 111 C420 142 381 164 338 164 C281 163 246 121 174 123 C112 125 76 174 99 205 C105 214 117 217 130 214 C121 224 109 226 99 220 Z'),
         ]),
    dict(slug='34-orbit-italic', name='Orbit Italic', ru='Наклонная орбита',
         idea='Собранная курсивная t внутри диагональной орбиты. Тонкая волна уравновешивает плотную букву.',
         type='Курсив · орбита', body=[
             shape('tilted-orbit', 'M421 222 C428 154 400 104 342 95 C257 82 151 162 113 256 C78 342 103 410 169 420 C245 432 339 377 396 309 C354 382 252 446 169 432 C92 420 63 343 103 248 C145 148 258 72 346 86 C408 96 438 151 421 222 Z'),
             shape('italic-t', 'M289 154 L306 154 L281 218 H330 L326 228 H277 L233 339 C224 361 231 371 244 371 C260 371 279 357 292 341 L297 346 C277 373 251 389 228 387 C199 385 196 363 210 328 L250 228 H216 L219 220 C248 207 268 181 289 154 Z', WHITE),
             shape('sweeping-crossbar', 'M78 276 C139 218 198 212 271 234 C336 253 381 261 440 223 C394 267 336 267 271 248 C196 225 137 226 78 276 Z'),
         ]),
    dict(slug='35-silk-loop', name='Silk Loop', ru='Шёлковая петля',
         idea='Буква t с высокой петлёй и широким мягким выходом. Знак похож на единый пластичный жест.',
         type='Петля · пластика', body=[
             shape('looped-t', 'M203 286 C236 229 253 178 263 143 C277 94 304 76 328 86 C357 98 338 140 300 172 C272 195 249 206 225 215 L217 210 C253 196 278 179 299 157 C328 126 341 103 326 94 C309 84 288 107 279 148 C265 211 243 259 217 305 C198 342 174 371 152 377 C129 383 115 368 123 348 C131 329 158 318 181 319 C155 323 136 335 133 350 C128 366 144 373 159 362 C176 348 191 313 203 286 Z', WHITE),
             shape('silk-crossbar', 'M100 228 C167 196 228 208 292 224 C346 237 382 234 419 205 C388 244 345 250 290 236 C219 217 166 208 100 228 Z'),
             shape('silk-tail', 'M152 377 C217 354 295 355 364 390 C319 374 268 367 225 372 C193 375 169 381 152 377 Z'),
         ]),
    dict(slug='36-sculpted-t', name='Sculpted T', ru='Скульптурная T',
         idea='Архитектурная T и короткая асимметричная лента. Меньше деталей для компактного аватара.',
         type='Антиква · баланс', body=[
             shape('t', SERIF_T, WHITE),
             shape('ribbon', 'M111 285 C170 294 214 266 256 233 C297 201 335 195 399 211 C345 211 312 221 275 252 C230 290 176 311 111 285 Z'),
         ]),
    dict(slug='37-breeze-circle', name='Breeze Circle', ru='Круг и дыхание',
         idea='Почти замкнутый круг с двумя лёгкими окончаниями. Вертикальная t задаёт спокойный центр.',
         type='Круг · спокойствие', body=[
             shape('upper-circle', 'M92 269 C67 173 138 81 235 72 C324 64 402 114 424 197 C395 121 324 79 240 85 C152 92 90 170 92 269 Z'),
             shape('lower-circle', 'M425 245 C454 343 377 431 280 441 C186 451 117 399 92 324 C125 391 192 431 276 427 C364 423 427 349 425 245 Z'),
             shape('slender-t', 'M268 133 C273 124 285 130 280 140 L247 324 C241 356 247 371 263 371 C281 370 298 355 310 340 C296 371 276 389 253 386 C223 383 222 357 229 321 Z', WHITE),
             shape('breathing-wave', 'M123 244 C178 207 228 213 286 227 C333 239 371 239 407 216 C373 248 331 250 285 237 C222 221 173 220 123 244 Z'),
         ]),
    dict(slug='38-tm-atelier', name='TM Atelier', ru='Монограмма с росчерком',
         idea='Высокая T и рукописная m соединены в личный знак. Контраст строгой формы и живой линии.',
         type='Монограмма · росчерк', body=[
             shape('serif-t', 'M101 134 H304 L307 182 H300 C289 151 272 145 232 145 V338 C232 365 238 373 263 378 V385 H151 V378 C178 373 184 365 184 338 V145 C140 145 122 154 109 182 H102 Z', WHITE),
             shape('script-m', 'M238 344 C252 303 263 271 279 257 C298 239 314 247 309 273 C307 283 303 293 299 304 C318 273 338 247 355 246 C376 246 373 266 366 288 C384 261 400 243 413 245 C434 250 412 284 404 305 C395 330 401 339 425 321 C414 341 393 350 386 335 C378 320 398 287 403 271 C406 261 402 258 396 264 C379 279 360 315 350 343 L338 343 L354 282 C358 266 355 260 347 268 C326 286 310 320 301 343 L287 343 L298 283 C303 260 299 257 290 265 C273 280 259 314 252 344 Z'),
         ]),
    dict(slug='39-crescent-serif', name='Crescent Serif', ru='T в полумесяце',
         idea='Чистая T и один широкий круговой жест. Лента переходит в орбиту, оставляя справа воздух.',
         type='Антиква · круговой жест', body=[
             shape('crescent', 'M386 125 C319 65 208 87 150 157 C89 232 100 331 171 382 C229 424 305 417 361 377 C300 431 219 440 156 391 C78 331 69 226 137 146 C200 71 315 53 386 125 Z'),
             shape('t', 'M176 156 H374 L377 201 H370 C359 172 345 167 300 167 V344 C300 364 307 371 330 375 V381 H230 V375 C252 371 259 364 259 344 V167 C215 167 199 176 184 201 H177 Z', WHITE),
             shape('crescent-return', 'M156 391 C211 357 283 356 339 375 C375 387 407 383 438 360 C411 390 375 400 337 386 C277 365 213 370 156 391 Z'),
         ]),
    dict(slug='40-continuum-t', name='Continuum T', ru='Непрерывная T',
         idea='Длинная петля одновременно формирует перекладину T и орбиту. Самый каллиграфичный вариант набора.',
         type='Каллиграфия · непрерывность', body=[
             shape('long-t', 'M305 139 C286 179 255 237 236 283 C217 328 193 370 165 388 C140 404 116 400 110 382 C102 358 125 335 151 326 C134 340 121 356 124 371 C127 386 146 388 162 376 C185 360 203 319 219 278 C237 232 266 177 286 141 Z', WHITE),
             shape('continuous-orbit', 'M91 238 C59 199 78 157 119 145 C166 131 216 161 269 165 C322 169 384 136 391 104 C399 74 363 70 336 96 C319 112 311 130 308 146 C305 125 316 101 333 87 C363 60 405 68 401 102 C397 140 333 178 269 177 C210 176 165 141 123 151 C87 159 74 194 94 221 C108 240 139 237 157 223 C142 248 110 257 91 238 Z'),
             shape('lower-flourish', 'M165 388 C224 380 290 348 358 290 C319 340 250 392 199 400 C183 403 171 397 165 388 Z'),
         ]),
]


def master(concept, light=False):
    body = '\n    '.join(concept['body'])
    if light:
        body = body.replace(WHITE, INK)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-labelledby="logo-title logo-description">
  <title id="logo-title">Tatsi in motion — {escape(concept['name'])}</title>
  <desc id="logo-description">{escape(concept['idea'])} Editable vector outlines; transparent background.</desc>
  <g id="{concept['slug']}-artwork">
    {body}
  </g>
</svg>
'''


for folder in ('svg', 'svg-light', 'preview'):
    (ROOT / folder).mkdir(exist_ok=True)
for concept in concepts:
    (ROOT / 'svg' / (concept['slug'] + '.svg')).write_text(master(concept))
    (ROOT / 'svg-light' / (concept['slug'] + '.svg')).write_text(master(concept, True))
(ROOT / 'concepts-31-40.json').write_text(json.dumps([{k: v for k, v in c.items() if k != 'body'} for c in concepts], ensure_ascii=False, indent=2) + '\n')

cards = []
for c in concepts:
    n = c['slug'][:2]
    cards.append(f'''<article><div class="dark"><span class="number">{n}</span><img src="../svg/{c['slug']}.svg" alt="{c['name']}"></div><div class="light"><img src="../svg-light/{c['slug']}.svg" alt="На светлом фоне"><div><h2>{c['name']}</h2><p>{c['ru']}</p></div></div></article>''')
overview = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Tatsi in motion — 31–40</title><style>*{box-sizing:border-box}body{margin:0;background:#f0f1ed;font-family:Arial,sans-serif;color:#142627}main{width:1800px;padding:45px 50px}header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:30px}.eyebrow{font-size:12px;letter-spacing:.16em;margin:0 0 12px;color:#53756a}h1{font-size:48px;font-weight:400;letter-spacing:-.04em;margin:0}header>p{font-size:14px;line-height:1.6;color:#53756a;margin:0}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:22px}article{overflow:hidden}.dark{height:315px;background:#142627;position:relative}.dark>img{width:100%;height:100%;padding:10px}.number{position:absolute;left:16px;top:16px;font-size:12px;color:#bcf7f3}.light{height:130px;display:flex;align-items:center;background:#fff;padding:10px 13px;gap:8px}.light>img{width:88px;height:110px;flex-shrink:0}h2{font-size:17px;font-weight:400;margin:0 0 8px}p{font-size:11px;color:#6c7c73;margin:0;line-height:1.5}footer{font-size:12px;color:#53756a;display:flex;justify-content:space-between;margin-top:28px}</style></head><body><main><header><div><p class="eyebrow">LOGO EXPLORATION / 31—40</p><h1>Tatsi in motion.</h1></div><p>Каллиграфия · орбиты · плавные ленты<br>10 новых вариантов по вашему референсу</p></header><section class="grid">CARDS</section><footer><span>Белый + #bcf7f3 · отдельные SVG · прозрачный фон</span><span>Внизу — версии для светлого фона</span></footer></main></body></html>'''
(ROOT / 'preview' / 'reference-31-40.html').write_text(overview.replace('CARDS', '\n'.join(cards)))
print('Created 10 primary SVGs, 10 matching light-background SVGs and an overview.')
