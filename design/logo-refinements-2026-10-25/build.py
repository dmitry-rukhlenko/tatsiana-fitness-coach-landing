"""Draw editable refinements of the three user-selected logo directions."""
from pathlib import Path
import html
import json
import math

ROOT = Path(__file__).resolve().parent
MINT, WHITE, INK = '#bcf7f3', '#ffffff', '#142627'
concepts = []

def path(name, d, fill=MINT, extra=''):
    return f'<path id="{name}" d="{d}" fill="{fill}" {extra}/>'

def polygon(points):
    return 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in points) + ' Z'

def orbit(weight=10, rx=184, ry=188, start=-35, sweep=-325, tilt=0, center=(256,256)):
    outside, inside = [], []
    rot = math.radians(tilt)
    for i in range(151):
        t = i / 150
        angle = math.radians(start + sweep * t)
        width = weight * (.45 + .55 * math.sin(math.pi * t)**.7) * (1 - t**15) + .15
        x, y = rx*math.cos(angle), ry*math.sin(angle)
        nx, ny = math.cos(angle), math.sin(angle)
        for points, sign in [(outside,1), (inside,-1)]:
            px, py = x + sign*width*.5*nx, y + sign*width*.5*ny
            points.append((center[0]+px*math.cos(rot)-py*math.sin(rot),center[1]+px*math.sin(rot)+py*math.cos(rot)))
    return path('open-orbit', polygon(outside + inside[::-1]))

LETTERS = {
 'script': 'M303 137 C311 126 322 132 314 146 C282 193 249 253 228 305 C212 344 211 374 239 374 C261 373 284 354 305 330 C286 370 254 394 228 390 C190 386 194 350 210 311 C235 247 271 185 303 137 Z',
 'fine': 'M302 139 C307 133 312 136 308 143 C278 190 249 252 227 309 C211 349 213 376 235 377 C257 377 278 361 298 340 C279 369 254 387 231 386 C203 385 200 356 215 316 C239 251 274 186 302 139 Z',
 'bold': 'M291 136 C301 121 319 130 311 146 C282 193 251 254 234 306 C221 346 220 368 243 369 C263 368 289 347 311 321 C293 363 263 394 233 393 C190 392 186 356 204 308 C229 242 262 180 291 136 Z',
 'italic': 'M272 158 L326 125 L302 183 L338 183 L334 193 L298 193 L243 321 C231 350 225 374 244 374 C263 374 282 358 302 341 C281 371 257 392 232 390 C202 388 206 358 217 331 L274 194 L245 194 L249 185 L278 185 L287 163 Z',
 'upright': 'M271 138 C274 127 284 129 282 140 L253 317 C246 357 245 379 267 377 C285 376 302 359 317 343 C301 371 279 390 257 389 C222 387 228 351 233 320 Z',
 'loop': 'M265 204 C264 165 287 119 311 121 C337 124 319 166 282 199 C258 245 239 291 228 325 C218 356 218 377 239 375 C259 374 282 356 302 334 C282 369 257 391 230 389 C200 387 199 361 214 319 C230 272 251 229 265 204 Z M282 184 C305 162 320 134 308 132 C296 130 285 158 282 184 Z',
 'round': 'M293 146 C299 135 312 140 306 153 C278 205 249 263 231 313 C221 340 219 363 238 367 C256 372 280 354 303 333 C283 364 258 386 232 381 C205 376 202 352 216 312 C235 258 267 194 293 146 Z',
}

def letter(kind='script', fill=WHITE):
    if kind == 'mono':
        return path('letter-t', 'M302 140 C266 193 233 266 218 317 C208 349 209 381 235 382 C257 382 283 362 303 339', 'none', f'stroke="{fill}" stroke-width="10" stroke-linecap="round"')
    return path('letter-t', LETTERS[kind], fill, 'fill-rule="evenodd"')

WAVES = {
 'soft':'M117 226 C164 185 221 188 286 201 C341 212 390 210 427 187 C398 219 349 225 288 212 C225 199 165 197 117 226 Z',
 'fine':'M118 224 C173 188 221 193 286 204 C342 215 387 214 425 194 C389 219 343 222 287 211 C222 198 172 196 118 224 Z',
 'bold':'M115 226 C167 177 225 185 288 198 C343 210 389 208 425 184 C395 220 348 231 286 218 C220 204 168 194 115 226 Z',
 'lift':'M117 238 C166 185 222 191 284 200 C342 209 390 196 423 175 C394 207 349 224 285 214 C220 204 167 199 117 238 Z',
 'quiet':'M124 219 C178 198 226 197 284 204 C336 210 382 211 418 196 C381 218 337 219 283 211 C224 203 179 205 124 219 Z',
 'slender':'M123 230 C171 181 224 192 288 210 C341 225 385 215 420 190 C389 222 344 232 288 217 C225 199 173 190 123 230 Z',
 'round':'M125 224 C170 190 222 190 281 201 C335 211 381 211 415 193 C383 219 339 222 280 213 C222 202 173 200 125 224 Z'
}

def lower_flourish(kind=0):
    shapes = [
      'M214 410 C244 371 277 386 312 391 C361 398 402 364 426 329 C403 378 362 410 314 402 C276 395 247 382 214 410 Z',
      'M211 406 C244 378 277 388 313 392 C358 397 398 369 422 338 C396 379 357 403 313 398 C278 393 245 384 211 406 Z',
      'M205 414 C241 368 278 382 313 387 C361 393 399 367 427 330 C403 383 364 413 313 406 C274 400 240 382 205 414 Z',
      'M222 411 C250 383 280 390 312 393 C355 398 390 374 414 346 C392 383 355 405 312 401 C276 397 249 389 222 411 Z',
      'M218 406 C249 386 280 393 309 394 C345 396 381 380 411 355 C383 386 346 402 310 400 C278 398 248 391 218 406 Z',
      'M208 411 C239 370 275 391 310 395 C354 401 392 376 419 344 C391 387 354 412 309 404 C270 397 243 379 208 411 Z',
      'M226 405 C251 382 281 387 308 391 C342 397 377 382 402 361 C379 389 345 407 309 400 C275 393 250 389 226 405 Z',
    ]
    return '<g transform="translate(0 9)">'+path('lower-flourish',shapes[kind])+'</g>'

def add(code, name, description, letter_style, weight, artwork):
    concepts.append(dict(code=code,slug=code.lower(),group=code[0],name=name,idea=description,letter_style=letter_style,weight=weight,artwork=artwork))

A = [
 ('A1','Мягкая классика','Ближе к первому референсу: мягкая t, средняя окружность и выразительная нижняя волна.','script',10,'soft',184,188,-35,0),
 ('A2','Тонкое перо','Тоньше буква и волны; лёгкая окружность делает знак более деликатным.','fine',5,'fine',184,188,-35,0),
 ('A3','Уверенный штрих','Более плотная t, толстая дуга и широкая волна — вариант для небольших размеров.','bold',16,'bold',182,186,-35,0),
 ('A4','Курсивная антиква','У t появляется клиновидное начало и засечка. Волна направлена чуть выше.','italic',7,'lift',184,188,-32,0),
 ('A5','Вертикальная t','Буква стоит прямее; спокойная перекладина и узкий высокий овал.','upright',8,'quiet',170,194,-34,0),
 ('A6','Петля пера','Каллиграфическая петля вместо обычной вершины t и более текучая волна.','loop',8,'slender',184,188,-39,-4),
 ('A7','Компактная мягкость','Короткая округлая t, округлый контур и сдержанный нижний росчерк.','round',12,'round',179,181,-37,0),
]
for i,(code,name,idea,kind,weight,wave,rx,ry,start,tilt) in enumerate(A):
    add(code,name,idea,kind,weight,orbit(weight,rx,ry,start,-360-start,tilt)+letter(kind,MINT)+path('crossbar',WAVES[wave])+lower_flourish(i))

B = [
 ('B1','Лёгкая орбита','Сохраняет любимую композицию: белая каллиграфическая t и мятная волна.','script',10,'soft',184,188,-35,0),
 ('B2','Контраст пера','Тонкая орбита вокруг более плотной белой буквы; контраст толщин усилен.','bold',5,'fine',183,187,-35,0),
 ('B3','Ровная линия','Почти одинаковая толщина белого штриха и мятной окружности. Современная спокойная t.','mono',9,'quiet',184,188,-35,0),
 ('B4','Курсив в эллипсе','Антиквенная t с засечками и диагональная эллиптическая орбита.','italic',9,'lift',172,193,-30,15),
 ('B5','Плотный аватар','Усиленная буква, толстая дуга и компактные пропорции для аватара.','bold',17,'bold',179,182,-38,0),
 ('B6','Рукописная петля','Верхняя петля добавляет личный характер; тонкая дуга оставляет больше воздуха.','loop',6,'slender',184,190,-38,-5),
 ('B7','Высокая вертикаль','Более прямая и узкая белая t, вытянутый овал и спокойная волна.','upright',8,'quiet',169,194,-33,0),
]
for code,name,idea,kind,weight,wave,rx,ry,start,tilt in B:
    add(code,name,idea,kind,weight,orbit(weight,rx,ry,start,-360-start,tilt)+letter(kind)+path('crossbar',WAVES[wave]))

# These silhouettes keep the broad swept cap and curved descending stem of the
# brush reference. Their widths, curvature and endings are deliberately distinct.
CAPS = {
 'balanced':'M64 157 C98 124 196 119 292 116 C371 114 420 98 453 78 C422 112 365 133 292 141 C207 150 134 143 105 159 C93 167 102 179 130 176 C94 194 62 185 60 169 C59 165 60 161 64 157 Z',
 'fine':'M69 157 C109 129 209 128 300 120 C370 113 418 99 453 80 C416 112 366 127 300 135 C212 145 128 141 101 160 C89 168 105 174 128 171 C96 183 69 177 66 167 C64 163 65 160 69 157 Z',
 'bold':'M64 151 C106 111 204 115 300 111 C369 109 418 97 452 80 C419 119 365 140 300 148 C223 158 145 152 114 165 C99 172 105 185 135 182 C91 207 56 188 56 169 C56 163 59 157 64 151 Z',
 'slant':'M66 177 C108 137 204 132 296 119 C365 110 415 91 450 66 C423 107 369 132 303 145 C219 162 147 158 112 178 C100 185 111 194 139 188 C100 210 63 203 61 188 C60 184 62 180 66 177 Z',
 'ribbon':'M70 159 C117 125 211 127 302 117 C366 110 417 98 450 78 C415 115 360 132 301 139 C215 150 143 141 109 159 C94 167 107 177 131 175 C103 190 74 184 66 172 C62 167 64 163 70 159 Z',
 'gesture':'M67 162 C111 121 190 116 278 116 C352 116 410 103 451 77 C422 114 368 143 287 145 C204 147 134 142 106 160 C95 169 115 180 145 173 C109 198 62 191 61 173 C60 169 62 165 67 162 Z',
}
STEMS = {
 'balanced':'M281 139 C235 174 201 218 207 272 C212 318 238 362 224 408 C214 443 194 468 174 485 C207 445 215 414 207 375 C197 327 171 286 183 238 C194 193 236 158 281 139 Z',
 'fine':'M280 137 C238 173 207 215 209 260 C211 305 234 352 224 397 C216 433 196 460 176 480 C204 442 215 412 209 375 C202 329 182 285 190 246 C198 200 235 165 280 137 Z',
 'bold':'M286 141 C242 177 213 216 216 257 C220 303 243 344 232 387 C222 427 201 452 179 470 C208 428 215 402 206 365 C195 321 170 284 179 242 C189 193 236 158 286 141 Z',
 'slant':'M301 139 C254 176 219 220 218 267 C218 310 232 349 215 390 C201 423 176 450 150 467 C185 431 203 398 200 360 C195 316 185 281 194 244 C204 204 247 159 301 139 Z',
 'ribbon':'M287 136 C241 173 201 215 201 257 C202 296 223 333 221 369 C219 415 201 449 178 474 C207 429 212 396 202 358 C191 319 172 284 181 245 C191 201 234 158 287 136 Z',
 'gesture':'M279 139 C233 178 202 219 213 264 C224 310 249 340 234 387 C221 427 196 461 171 480 C207 435 217 401 207 368 C191 322 168 285 182 240 C195 193 236 156 279 139 Z',
}

def brush_texture():
    # Narrow closed contours are cut out with even-odd filling, not white paint.
    cap_holes = [
      'M94 162 C144 130 241 137 344 120 C242 142 148 138 94 162 Z',
      'M112 169 C159 145 242 150 341 128 C250 153 166 148 112 169 Z',
      'M172 138 C253 125 334 128 405 102 C345 129 254 134 172 138 Z',
      'M242 137 C307 133 358 121 401 110 C357 127 305 138 242 137 Z',
    ]
    stem_holes = [
      'M249 162 C210 198 195 233 199 261 C192 236 205 195 249 162 Z',
      'M201 286 C211 328 229 363 217 408 C226 365 207 331 201 286 Z',
      'M188 235 C181 265 187 292 198 318 C184 291 178 265 188 235 Z',
      'M212 335 C222 367 220 391 214 409 C218 385 216 365 212 335 Z',
    ]
    hairs = [
      'M94 148 C183 118 319 126 425 91 C336 125 182 124 94 148 Z',
      'M137 142 C227 116 364 124 444 78 C376 121 241 126 137 142 Z',
      'M151 151 C248 141 358 143 420 115 C360 146 250 147 151 151 Z',
      'M237 169 C204 199 177 231 178 266 C174 232 199 198 237 169 Z',
      'M184 278 C190 321 217 367 204 408 C213 366 186 323 184 278 Z',
      'M227 384 C218 431 191 464 165 484 C190 461 215 429 227 384 Z',
    ]
    return path('brush-cap',CAPS['balanced']+' '+' '.join(cap_holes),extra='fill-rule="evenodd"')+path('brush-stem',STEMS['balanced']+' '+' '.join(stem_holes),extra='fill-rule="evenodd"')+''.join(path(f'bristle-{i+1}',d) for i,d in enumerate(hairs))

C = [
 ('C1','Чистая кисть','Сохраняет пластику кистевого референса, но убирает мелкую фактуру: плавная шапка и S-образная ножка.','balanced',0),
 ('C2','Тонкая тушь','Более тонкий мазок, узкая ножка и мягкая шапка — лёгкая каллиграфическая версия.','fine',0),
 ('C3','Широкий мазок','Шапка и ножка плотнее, хвост короче. Самый устойчивый кистевой силуэт в малом размере.','bold',0),
 ('C4','Диагональный жест','Приподнятый правый край и усиленный наклон ножки добавляют ощущение движения.','slant',0),
 ('C5','Сухая кисть','Тонкие просветы и отдельные волоски повторяют характер кисти. Фактура полностью векторная.','balanced',1),
 ('C6','Шёлковая лента','Плавное изменение ширины и более спокойная S-образная ножка напоминают мягкую ленту.','ribbon',0),
 ('C7','Свободная подпись','Широкая живая шапка и выразительный изгиб ножки; небольшие отдельные штрихи на окончаниях.','gesture',0),
]
for code,name,idea,kind,texture in C:
    art = brush_texture() if texture else path('brush-cap',CAPS[kind])+path('brush-stem',STEMS[kind])
    if code == 'C7':
        art += path('cap-tip','M278 128 C352 126 403 109 450 82 C413 111 352 135 278 128 Z')
        art += path('stem-tip','M222 396 C208 432 185 463 163 480 C188 455 211 422 222 396 Z')
    # Lift and center the tall source gesture to leave clear space on all sides.
    art = '<g transform="translate(0 -15)">'+art+'</g>'
    add(code,name,idea,'brush-'+kind,0,art)

for c in concepts:
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-labelledby="title desc">
<title id="title">Tatsi in motion — {c['code']} · {c['name']}</title>
<desc id="desc">{html.escape(c['idea'])} Editable vector artwork; transparent background.</desc>
<g id="artwork">{c['artwork']}</g></svg>
'''
    (ROOT/'svg'/f"{c['slug']}.svg").write_text(svg)
    (ROOT/'svg-light'/f"{c['slug']}.svg").write_text(svg.replace(WHITE,INK))

metadata=[{k:v for k,v in c.items() if k!='artwork'} for c in concepts]
(ROOT/'concepts.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
groups={'A':('Мятная t + две волны','Тонкость пера · характер буквы · пластика окружности'), 'B':('Белая t + открытая орбита','Контраст штрихов · наклон · читаемость в аватаре'), 'C':('Кистевая T','Чистый силуэт · ширина мазка · векторная фактура')}
css='''*{box-sizing:border-box}body{margin:0;background:#eff2ee;color:#142627;font-family:Arial,sans-serif}main{padding:38px 42px}.eyebrow{font-size:11px;letter-spacing:.16em;color:#4b6861;text-transform:uppercase}h1{font-size:36px;font-weight:500;margin:12px 0 8px}header>p{font-size:14px;color:#4b6861}section{margin-top:32px}.group-title{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:14px}h2{font-size:21px;font-weight:500;margin:0}.group-title p{font-size:13px;color:#4b6861;margin:0}.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}article{background:white}article .art{position:relative;background:#142627;padding:8px}article .art img{display:block;width:100%;height:auto}b.code{position:absolute;left:12px;top:12px;font-size:12px;font-weight:500;color:#bcf7f3}.caption{padding:13px 11px;display:flex;align-items:center;gap:8px}.caption img{width:44px;height:44px;flex-shrink:0}.caption p{font-size:12px;margin:0;line-height:1.4}footer{margin-top:28px;font-size:12px;color:#4b6861}'''
sections=[]
for group,(title,subtitle) in groups.items():
    cards=''.join(f'''<article><div class="art"><b class="code">{c['code']}</b><img src="../svg/{c['slug']}.svg" alt="{c['name']}"></div><div class="caption"><img src="../svg-light/{c['slug']}.svg" alt="На светлом фоне"><p>{c['name']}</p></div></article>''' for c in concepts if c['group']==group)
    section=f'<section><div class="group-title"><h2>{group} / {title}</h2><p>{subtitle}</p></div><div class="grid">{cards}</div></section>'
    sections.append(section)
    (ROOT/'preview'/f'group-{group.lower()}.html').write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><style>{css}</style><main><header><p class="eyebrow">Tatsi in motion / 7 refinements</p><h1>{title}</h1></header>{section}<footer>Белый + #bcf7f3 · Внизу показана версия на светлом фоне · Все контуры редактируются</footer></main></html>')
(ROOT/'preview/overview.html').write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><style>{css}</style><main><header><p class="eyebrow">Tatsi in motion / 3 directions × 7 refinements</p><h1>Три направления. Двадцать один вариант.</h1><p>По вашим выбранным образцам · форма буквы, толщина штриха, наклон и характер линии</p></header>{"".join(sections)}<footer>Белый + #bcf7f3 · Отдельные SVG и PNG · Тёмная подложка не входит в файл логотипа</footer></main></html>')
print('Created 21 vector masters, 21 light versions and 3 overview groups.')
