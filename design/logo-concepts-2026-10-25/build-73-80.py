"""Build concepts 73-80: more variants of the dark ring-t mark (48), from the brainstorm list.

73 escape        the wave leaves the ring
74 signature     the ring flies off into a swash
75 echo          hairline echo under the wave
76 ring curl     the ring's end curls inward
77 lower swash   signature-like flourish under the t
78 halo          a second, thinner ring: a soft double halo
79 tilt          the t leans 8° with the wave straightened — more momentum
80 through       the wave passes through the ring on both sides
Run:  python3 build-73-80.py
"""
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import calligraphy as C  # noqa: E402
from calligraphy import BRAND_MINT as MINT, ZAPF, taper, curl_from, wave_with_curl  # noqa: E402

WHITE = '#ffffff'
SET_TITLE = '73—80 · ещё варианты тёмного знака 48: идеи из брейншторма'
concepts = []


def add(slug, name, ru, idea, kind, body):
    concepts.append({'slug': slug, 'name': name, 'ru': ru, 'idea': idea, 'type': kind,
                     'on_dark': {}, 'light_card': False, 'set_title': SET_TITLE})
    (ROOT / 'svg' / f'{slug}.svg').write_text(C.master(f'Tatsi in motion — {name}', body,
                                                       note='Designed for dark surfaces: white letter, brand mint #bcf7f3.'))


def ring(width=6, a0=-15, a1=290, cx=256, cy=256, r=200):
    return C.ellipse_arc(cx, cy, r, r, a0, a1, width=width, color=MINT)


def script_t(cx=256, cy=256, dx=6, dy=-6, fill=WHITE, pid='t'):
    return C.placed(ZAPF, 't', C.size_for_height(ZAPF, 't', 270), cx, cy, fill=fill, pid=pid, dx=dx, dy=dy)


CROSS = ((84, 236), (170, 196), (300, 268), (468, 220))


def crossbar(w=8, fill=MINT):
    return taper(*CROSS, w, fill=fill, pid='wave')


add('73-dark-escape', 'Dark · escape', 'Тёмный, волна за кольцо',
    'Волна начинается в кольце и уходит за его край, заканчиваясь завитком снаружи.', 'Тёмный · свобода', [
        ring(cx=232, r=190),
        wave_with_curl((90, 240), (170, 200), (300, 266), (486, 214), 8, 20, 330, 0.75, MINT, split=0.8),
        script_t(232, 256),
    ])

end_a = 300
end = (256 + 200 * math.cos(math.radians(end_a)), 256 + 200 * math.sin(math.radians(end_a)))
end_phi = math.degrees(math.atan2(math.cos(math.radians(end_a)), -math.sin(math.radians(end_a))))
add('74-dark-signature', 'Dark · signature ring', 'Тёмный, кольцо-подпись',
    'Кольцо одним движением с росчерком наружу у разрыва; белая t, мятная волна.', 'Тёмный · росчерк', [
        C.brush_ring(256, 256, 200, -10, end_a, 12, MINT, profile=lambda t: 0.45 + 0.55 * math.sin(math.pi * t) ** 1.2),
        curl_from(end, end_phi, 64, 95, 0.55, 6, MINT, pid='swash', ccw=False, steps=40),
        crossbar(), script_t(),
    ])

add('75-dark-echo', 'Dark · echo', 'Тёмный, эхо волны',
    'Тонкая линия-эхо под волной, как во втором референсе; остальное без изменений.', 'Тёмный · эхо', [
        ring(), crossbar(), taper((120, 262), (190, 226), (300, 290), (430, 250), 3, fill=MINT, pid='wave-echo'), script_t(),
    ])

ring_end = (256 + 200 * math.cos(math.radians(290)), 256 + 200 * math.sin(math.radians(290)))
ring_phi = math.degrees(math.atan2(math.cos(math.radians(290)), -math.sin(math.radians(290))))
add('76-dark-ring-curl', 'Dark · ring curl', 'Тёмный, завиток кольца',
    'Верхний конец кольца закручивается внутрь маленькой спиралью.', 'Тёмный · завиток', [
        ring(), curl_from(ring_end, ring_phi, 26, 300, 0.7, 6, MINT, pid='ring-curl', ccw=False), crossbar(), script_t(),
    ])

add('77-dark-lower-swash', 'Dark · lower swash', 'Тёмный, росчерк внизу',
    'Под буквой росчерк с петелькой, как подпись; волна-перекладина прежняя.', 'Тёмный · подпись', [
        ring(), crossbar(), wave_with_curl((196, 448), (268, 478), (350, 440), (440, 392), 6, 20, 340, 0.75, MINT, pid='wave-low'), script_t(),
    ])

add('78-dark-halo', 'Dark · halo', 'Тёмный, двойное кольцо',
    'Второе, тоньшее кольцо чуть больше первого с собственным разрывом: мягкий ореол вокруг буквы.', 'Тёмный · ореол', [
        ring(6), C.ellipse_arc(256, 256, 214, 214, 40, 250, width=2.5, color=MINT, pid='halo'), crossbar(), script_t(),
    ])

add('79-dark-tilt', 'Dark · tilt', 'Тёмный, наклон',
    'Буква наклонена ещё на 8°, волна спрямлена и приподнята к концу — больше разбега.', 'Тёмный · разбег', [
        ring(),
        taper((84, 244), (180, 214), (300, 240), (468, 190), 8, fill=MINT, pid='wave'),
        f'<g id="t-tilt" transform="rotate(8 256 256)">{script_t(dx=2)}</g>',
    ])

add('80-dark-through', 'Dark · through', 'Тёмный, волна сквозь кольцо',
    'Волна длиннее кольца и выходит за него с обеих сторон: движение проходит сквозь форму.', 'Тёмный · сквозь', [
        ring(6, cx=256, r=186),
        taper((28, 240), (150, 198), (330, 272), (496, 212), 8, fill=MINT, pid='wave'),
        script_t(),
    ])

(ROOT / 'concepts-73-80.json').write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + '\n')
cards = ''.join(
    f'<div class="card"><img src="../svg/{c["slug"]}.svg"><div class="s"><img src="../svg/{c["slug"]}.svg" style="width:48px;height:48px"></div><div class="n">{c["slug"][:2]} · {c["name"]}</div></div>'
    for c in concepts)
(ROOT / 'preview' / 'variations-73-80.html').write_text(
    '<!doctype html><meta charset="utf-8"><title>73-80</title><style>body{margin:0;background:#0b1516;font:13px Helvetica,Arial;color:#a3b7b3;padding:26px}'
    '.row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{border-radius:10px;padding:12px;background:#142627}'
    '.card img{width:100%;height:300px;object-fit:contain;display:block}.n{font-size:12px;margin-top:8px}.s{display:flex;gap:8px;align-items:flex-end;margin-top:6px;height:48px}</style>'
    f'<div class="row">{cards}</div>')
print(f'Built {len(concepts)} masters (73-80)')
