"""Build concepts 62-68: the liked marks with one small flourish curl added in different places.

Run:  python3 build-62-68.py
"""
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import calligraphy as C  # noqa: E402
from calligraphy import INK, MINT_ON_WHITE as MINT, BRAND_MINT, ZAPF, taper, taper_fn, cubic, curl_from, wave_with_curl  # noqa: E402

WHITE = '#ffffff'
SET_TITLE = '62—68 · маленькая завитушка: где она смотрится естественнее'
ON_DARK = {MINT: BRAND_MINT, INK: WHITE}
concepts = []


def add(slug, name, ru, idea, kind, body, on_dark=None, light_card=True):
    concepts.append({'slug': slug, 'name': name, 'ru': ru, 'idea': idea, 'type': kind,
                     'on_dark': on_dark or {}, 'light_card': light_card, 'set_title': SET_TITLE})
    (ROOT / 'svg' / f'{slug}.svg').write_text(C.master(f'Tatsi in motion — {name}', body))


def ring(width=6, color=MINT, a0=-15, a1=290):
    return C.ellipse_arc(256, 256, 200, 200, a0, a1, width=width, color=color)


def script_t(fill=MINT):
    return C.placed(ZAPF, 't', C.size_for_height(ZAPF, 't', 270), 256, 256, fill=fill, pid='t', dx=6, dy=-6)


CROSS = ((84, 236), (170, 196), (300, 268), (468, 220))
LOW = ((196, 448), (268, 478), (350, 440), (440, 392))


def crossbar(fill=MINT):
    return taper(*CROSS, 8, fill=fill, pid='wave')


def lower_wave(fill=MINT):
    return taper(*LOW, 6, fill=fill, pid='wave-low')


# 62 — the crossbar wave ends in a small curl that turns back over itself
add('62-curl-wave', 'Curl · wave tail', 'Завиток на волне',
    'Волна-перекладина заканчивается маленькой петелькой, завёрнутой назад, как росчерк пера.',
    'Завиток · волна', [ring(), wave_with_curl(*CROSS, 8, 22, 330, 0.75, MINT), lower_wave(), script_t()], ON_DARK)

# 63 — the ring's upper end curls inward at the gap
ring_end_phi = math.degrees(math.atan2(math.cos(math.radians(290)), -math.sin(math.radians(290))))
ring_end = (256 + 200 * math.cos(math.radians(290)), 256 + 200 * math.sin(math.radians(290)))
add('63-curl-ring', 'Curl · ring end', 'Завиток на кольце',
    'Верхний конец кольца у разрыва закручивается внутрь небольшой спиралью.',
    'Завиток · кольцо', [ring(), curl_from(ring_end, ring_end_phi, 26, 300, 0.7, 6, MINT, pid='ring-curl', ccw=False), crossbar(), lower_wave(), script_t()], ON_DARK)

# 64 — the lower wave becomes a signature-like flourish with a loop
add('64-curl-lower', 'Curl · lower flourish', 'Завиток внизу',
    'Нижняя волна превращается в росчерк с петелькой — как подпись под буквой.',
    'Завиток · подпись', [ring(), crossbar(), wave_with_curl(*LOW, 6, 20, 340, 0.75, MINT, pid='wave-low', ccw=True), script_t()], ON_DARK)

# 65 — brush T: a curl at the end of the top stroke
TOP = ((64, 206), (150, 150), (330, 140), (492, 96))
STEM = ((322, 170), (300, 262), (238, 340), (200, 500))


def top_profile(t):
    return min(1.0, t * 7) * (1 - t) ** 0.75


def stem_profile(t):
    return (0.5 + 0.5 * math.sin(math.pi * min(1.0, t * 1.4))) * (1 - t) ** 0.45


def brush_parts(top_fill=MINT, stem_fill=MINT):
    return [taper_fn(lambda t: cubic(*STEM, t), 34, stem_profile, stem_fill, 'stem'),
            taper_fn(lambda t: cubic(*TOP, t), 44, top_profile, top_fill, 'top')]


top_phi = math.degrees(math.atan2(TOP[3][1] - TOP[2][1], TOP[3][0] - TOP[2][0]))
add('65-curl-brush-tail', 'Curl · brush tail', 'Завиток на хвосте T',
    'Хвост верхнего мазка кистевой T завершается маленьким завитком вверх.',
    'Завиток · кисть', brush_parts() + [curl_from((478, 100), top_phi, 18, 320, 0.7, 5, MINT, pid='tail-curl', ccw=True)], ON_DARK)

# 66 — brush T: a hook-curl at the foot of the stem
stem_phi = math.degrees(math.atan2(STEM[3][1] - STEM[2][1], STEM[3][0] - STEM[2][0]))
add('66-curl-brush-foot', 'Curl · brush foot', 'Завиток у ножки T',
    'Ножка кистевой T заканчивается крючком-завитком вправо, как при отрыве кисти.',
    'Завиток · кисть', brush_parts() + [curl_from((203, 486), stem_phi, 20, 300, 0.7, 7, MINT, pid='foot-curl', ccw=True)], ON_DARK)

# 67 — the dark colourway of 62
add('67-curl-wave-dark', 'Curl · wave tail, dark', 'Завиток на волне, тёмный',
    'Вариант 62 для тёмного фона: белая t, мятное кольцо и волна с петелькой.',
    'Завиток · тёмный', [ring(6, BRAND_MINT), wave_with_curl(*CROSS, 8, 22, 330, 0.75, BRAND_MINT), script_t(WHITE)], light_card=False)

# 68 — both curls at once: ring end and wave tail
add('68-curl-double', 'Curl · double', 'Два завитка',
    'И кольцо, и волна с завитками — самая декоративная версия, для сравнения меры.',
    'Завиток · два', [ring(), curl_from(ring_end, ring_end_phi, 26, 300, 0.7, 6, MINT, pid='ring-curl', ccw=False),
                      wave_with_curl(*CROSS, 8, 22, 330, 0.75, MINT), lower_wave(), script_t()], ON_DARK)

(ROOT / 'concepts-62-68.json').write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + '\n')

cards = ''.join(
    f'<div class="card{" dark" if not c["light_card"] else ""}"><img src="../svg/{c["slug"]}.svg"><div class="s"><img src="../svg/{c["slug"]}.svg" style="width:48px;height:48px"></div><div class="n">{c["slug"][:2]} · {c["name"]}</div></div>'
    for c in concepts)
(ROOT / 'preview' / 'variations-62-68.html').write_text(
    '<!doctype html><meta charset="utf-8"><title>62-68</title><style>body{margin:0;background:#e9eeeb;font:13px Helvetica,Arial;color:#3a4a47;padding:26px}'
    '.row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{border-radius:10px;padding:12px;background:#fff;border:1px solid #d8ddd9}'
    '.card.dark{background:#142627;border-color:#142627;color:#a3b7b3}.card img{width:100%;height:300px;object-fit:contain;display:block}'
    '.n{font-size:12px;margin-top:8px}.s{display:flex;gap:8px;align-items:flex-end;margin-top:6px;height:48px}</style>'
    f'<div class="row">{cards}</div>')
print(f'Built {len(concepts)} masters (62-68)')
