"""Build concepts 41-61: seven variations on each of the three marks the owner liked.

A  41-47  ring + script t + wave, mint on white
B  48-54  the same mark for dark surfaces (white t, brand-mint ring and wave)
C  55-61  brush-stroke calligraphic T
Varied: letter font (Zapfino, Snell Roundhand, Savoye, Apple Chancery), ring and wave weight, brush pressure,
one- vs two-colour. Run:  python3 build-41-61.py
"""
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import calligraphy as C  # noqa: E402
from calligraphy import INK, MINT_ON_WHITE as MINT, BRAND_MINT, ZAPF, SNELL, SNELL_LIGHT, SAVOYE, CHANCERY, taper, taper_fn, cubic  # noqa: E402

WHITE = '#ffffff'
SET_TITLE = '41—61 · развитие трёх понравившихся: кольцо с t на белом, на тёмном, кистевая T'
concepts = []


def add(slug, name, ru, idea, kind, body, on_dark=None, light_card=True):
    concepts.append({'slug': slug, 'name': name, 'ru': ru, 'idea': idea, 'type': kind,
                     'on_dark': on_dark or {}, 'light_card': light_card, 'set_title': SET_TITLE})
    (ROOT / 'svg' / f'{slug}.svg').write_text(C.master(f'Tatsi in motion — {name}', body,
                                                       note='Mint on white uses #86e3da; dark surfaces use ink #ffffff and brand mint #bcf7f3.' if light_card
                                                       else 'Designed for dark surfaces: white letter, brand mint #bcf7f3.'))


# ---------------------------------------------------------------- group A: ring + script t + wave (white)
ON_DARK_A = {MINT: BRAND_MINT, INK: WHITE}


def crossbar(w=8, fill=MINT):
    return taper((84, 236), (170, 196), (300, 268), (468, 220), w, fill=fill, pid='wave')


def lower_wave(w=6, fill=MINT):
    return taper((196, 448), (268, 478), (350, 440), (440, 392), w, fill=fill, pid='wave-low')


def ring(width=6, color=MINT, a0=-15, a1=290):
    return C.ellipse_arc(256, 256, 200, 200, a0, a1, width=width, color=color)


def script_t(font, height, fill=MINT, dx=6, dy=-6):
    return C.placed(font, 't', C.size_for_height(font, 't', height), 256, 256, fill=fill, pid='t', dx=dx, dy=dy)


add('41-ring-t-zapfino', 'Ring t · Zapfino', 'Кольцо, t Zapfino',
    'Исходный мотив: тонкое кольцо, каллиграфическая t Zapfino, волна-перекладина и нижняя волна. Всё мятным.',
    'Кольцо · Zapfino', [ring(6), crossbar(8), lower_wave(6), script_t(ZAPF, 270)], ON_DARK_A)

add('42-ring-t-snell', 'Ring t · Snell', 'Кольцо, t Snell',
    'Та же композиция с более плотной t Snell Roundhand: буква тяжелее, кольцо и волны прежние.',
    'Кольцо · Snell', [ring(6), crossbar(8), lower_wave(6), script_t(SNELL, 250, dx=4)], ON_DARK_A)

add('43-ring-t-savoye', 'Ring t · Savoye', 'Кольцо, t Savoye',
    'Самая лёгкая версия: тонкая t Savoye, кольцо и волны в полтора раза тоньше.',
    'Кольцо · Savoye', [ring(4), crossbar(5), lower_wave(4), script_t(SAVOYE, 290, dx=0)], ON_DARK_A)

add('44-ring-t-chancery', 'Ring t · Chancery', 'Кольцо, t Chancery',
    'Плотная версия: t Apple Chancery, кольцо и волны заметно толще, для мелких размеров и вышивки.',
    'Кольцо · Chancery', [ring(10), crossbar(11), lower_wave(8), script_t(CHANCERY, 250, dx=2)], ON_DARK_A)

add('45-ring-t-brush', 'Ring t · brush ring', 'Кольцо кистью',
    'Кольцо нарисовано кистью: толще слева, сходит на нет к разрыву. Буква Zapfino, волны как в исходном.',
    'Кольцо · кисть', [C.brush_ring(256, 256, 200, -15, 290, 15, MINT), crossbar(8), lower_wave(6), script_t(ZAPF, 270)], ON_DARK_A)

add('46-ring-t-single', 'Ring t · single wave', 'Кольцо, одна волна',
    'Без нижней волны: шире разрыв кольца, одна выразительная волна-перекладина, лёгкая t Snell.',
    'Кольцо · минимум', [ring(7, a0=-35, a1=270), crossbar(10), script_t(SNELL_LIGHT, 260, dx=4)], ON_DARK_A)

add('47-ring-t-ink', 'Ring t · ink', 'Кольцо, тёмная t',
    'Двухцветная версия: тёмная t, мятные кольцо и волны. Контрастнее на белом, печатается в две краски.',
    'Кольцо · два цвета', [ring(6), crossbar(8), lower_wave(6), script_t(ZAPF, 270, fill=INK)], ON_DARK_A)

# ---------------------------------------------------------------- group B: the dark version (white t, brand mint)
add('48-dark-t-zapfino', 'Dark ring t · Zapfino', 'Тёмный фон, t Zapfino',
    'Исходный тёмный вариант: мятное кольцо, белая t Zapfino, мятная волна-перекладина.',
    'Тёмный · Zapfino', [ring(6, BRAND_MINT), crossbar(8, BRAND_MINT), script_t(ZAPF, 270, fill=WHITE)], light_card=False)

add('49-dark-t-snell', 'Dark ring t · Snell', 'Тёмный фон, t Snell',
    'Белая плотная t Snell Roundhand в мятном кольце; волна прежняя.',
    'Тёмный · Snell', [ring(6, BRAND_MINT), crossbar(8, BRAND_MINT), script_t(SNELL, 250, fill=WHITE, dx=4)], light_card=False)

add('50-dark-t-savoye', 'Dark ring t · Savoye', 'Тёмный фон, t Savoye',
    'Тонкая белая t Savoye, кольцо и волна тоньше: воздушная версия для крупных форматов.',
    'Тёмный · Savoye', [ring(4, BRAND_MINT), crossbar(5, BRAND_MINT), script_t(SAVOYE, 290, fill=WHITE, dx=0)], light_card=False)

add('51-dark-t-chancery', 'Dark ring t · Chancery', 'Тёмный фон, t Chancery',
    'Плотная версия для аватаров: t Apple Chancery, кольцо и волна толще.',
    'Тёмный · Chancery', [ring(9, BRAND_MINT), crossbar(10, BRAND_MINT), script_t(CHANCERY, 250, fill=WHITE, dx=2)], light_card=False)

add('52-dark-t-inverted', 'Dark ring t · inverted', 'Тёмный фон, инверсия',
    'Цвета поменяны местами: мятная t, белые кольцо и волна.',
    'Тёмный · инверсия', [ring(6, WHITE), crossbar(8, WHITE), script_t(ZAPF, 270, fill=BRAND_MINT)], light_card=False)

add('53-dark-t-brush', 'Dark ring t · brush ring', 'Тёмный фон, кольцо кистью',
    'Кольцо кистью с переменной толщиной, белая t Zapfino, мятная волна.',
    'Тёмный · кисть', [C.brush_ring(256, 256, 200, -15, 290, 14, BRAND_MINT), crossbar(8, BRAND_MINT), script_t(ZAPF, 270, fill=WHITE)], light_card=False)

add('54-dark-t-two-waves', 'Dark ring t · two waves', 'Тёмный фон, две волны',
    'Белая волна-перекладина сливается с буквой, мятная нижняя волна и кольцо держат композицию.',
    'Тёмный · две волны', [ring(6, BRAND_MINT), crossbar(8, WHITE), lower_wave(6, BRAND_MINT), script_t(ZAPF, 270, fill=WHITE)], light_card=False)

# ---------------------------------------------------------------- group C: brush-stroke T
ON_DARK_C = {MINT: BRAND_MINT, INK: WHITE}


def top_profile(t):
    return min(1.0, t * 7) * (1 - t) ** 0.75


def stem_profile(t):
    return (0.5 + 0.5 * math.sin(math.pi * min(1.0, t * 1.4))) * (1 - t) ** 0.45


def brush_T(top_w=44, stem_w=34, top_pts=((64, 206), (150, 150), (330, 140), (492, 96)),
            stem_pts=((322, 170), (300, 262), (238, 340), (200, 500)), top_fill=MINT, stem_fill=MINT, dry=False):
    tp = lambda t: cubic(*top_pts, t)  # noqa: E731
    sp = lambda t: cubic(*stem_pts, t)  # noqa: E731
    parts = [taper_fn(sp, stem_w, stem_profile, stem_fill, 'stem'), taper_fn(tp, top_w, top_profile, top_fill, 'top')]
    if dry:
        # Dry-brush streaks: thinner parallel strokes offset from the main stroke, shorter than it.
        def shifted(fn, dx, dy):
            return lambda t: (fn(t)[0] + dx, fn(t)[1] + dy)
        parts += [
            taper_fn(shifted(tp, 0, -top_w * 0.34), top_w * 0.14, C.sine_profile, top_fill, 'top-streak-1', t0=0.3, t1=0.97),
            taper_fn(shifted(tp, 0, top_w * 0.36), top_w * 0.12, C.sine_profile, top_fill, 'top-streak-2', t0=0.4, t1=0.92),
            taper_fn(shifted(sp, stem_w * 0.42, 0), stem_w * 0.16, C.sine_profile, stem_fill, 'stem-streak-1', t0=0.08, t1=0.85),
            taper_fn(shifted(sp, -stem_w * 0.38, 0), stem_w * 0.12, C.sine_profile, stem_fill, 'stem-streak-2', t0=0.2, t1=0.95),
        ]
    return parts


add('55-brush-t', 'Brush T', 'Кистевая T',
    'Исходный мотив, чистой кистью: длинный верхний мазок с тонким хвостом и сужающаяся ножка.',
    'Кисть · чистая', brush_T(), ON_DARK_C)

add('56-brush-t-dry', 'Brush T · dry', 'Кистевая T, сухая кисть',
    'Тот же жест с прожилками сухой кисти вдоль обоих мазков — ближе к фактуре референса.',
    'Кисть · сухая', brush_T(dry=True), ON_DARK_C)

add('57-brush-t-bold', 'Brush T · bold', 'Кистевая T, жирная',
    'Сильный нажим: мазки в полтора раза толще, ножка короче. Читается в мелком размере.',
    'Кисть · нажим', brush_T(64, 50, ((70, 212), (160, 160), (330, 152), (470, 112)), ((322, 180), (300, 266), (242, 340), (206, 470))), ON_DARK_C)

add('58-brush-t-fine', 'Brush T · fine', 'Кистевая T, тонкая',
    'Лёгкий нажим: тонкие длинные мазки, хвост уходит дальше вправо, ножка ниже.',
    'Кисть · тонкая', brush_T(26, 20, ((60, 200), (150, 148), (330, 134), (504, 82)), ((322, 164), (300, 262), (232, 344), (190, 520))), ON_DARK_C)

add('59-brush-t-zapfino', 'Brush T · Zapfino', 'T Zapfino',
    'Готовая каллиграфическая T из Zapfino вместо мазка: тот же характер, но ровные контуры.',
    'Кисть · Zapfino', [C.placed(ZAPF, 'T', C.size_for_height(ZAPF, 'T', 300), 256, 256, fill=MINT, pid='T')], ON_DARK_C)

add('60-brush-t-snell', 'Brush T · Snell', 'T Snell',
    'Каллиграфическая T из Snell Roundhand: с петлёй и росчерком, более классическая.',
    'Кисть · Snell', [C.placed(SNELL_LIGHT, 'T', C.size_for_height(SNELL_LIGHT, 'T', 280), 256, 256, fill=MINT, pid='T')], ON_DARK_C)

add('61-brush-t-ink', 'Brush T · ink', 'Кистевая T, два цвета',
    'Двухцветная версия: тёмная ножка, мятный верхний мазок, сухая кисть.',
    'Кисть · два цвета', brush_T(dry=True, stem_fill=INK), ON_DARK_C)

(ROOT / 'concepts-41-61.json').write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + '\n')

# Comparison sheet: three rows, originals' colourways.
rows = [('A · кольцо, t и волна — на белом', concepts[0:7], False), ('B · то же для тёмного фона', concepts[7:14], True), ('C · кистевая T', concepts[14:21], False)]
html = ['<!doctype html><meta charset="utf-8"><title>41-61</title><style>body{margin:0;background:#e9eeeb;font:13px Helvetica,Arial;color:#3a4a47;padding:26px}'
        'h2{font-size:14px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;margin:18px 0 10px}.row{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}'
        '.card{border-radius:10px;padding:10px;background:#fff;border:1px solid #d8ddd9}.card.dark{background:#142627;border-color:#142627;color:#a3b7b3}'
        '.card img{width:100%;height:170px;object-fit:contain;display:block}.n{font-size:11px;margin-top:8px}.s{display:flex;gap:8px;align-items:flex-end;margin-top:6px;height:48px}</style>']
for title, cs, dark in rows:
    html.append(f'<h2>{title}</h2><div class="row">')
    for c in cs:
        html.append(f'<div class="card{" dark" if dark else ""}"><img src="../svg/{c["slug"]}.svg"><div class="s"><img src="../svg/{c["slug"]}.svg" style="width:48px;height:48px"><img src="../svg/{c["slug"]}.svg" style="width:24px;height:24px"></div><div class="n">{c["slug"][:2]} · {c["name"]}</div></div>')
    html.append('</div>')
(ROOT / 'preview' / 'variations-41-61.html').write_text('\n'.join(html))
print(f'Built {len(concepts)} masters (41-61), concepts-41-61.json and preview/variations-41-61.html')
