"""Build concepts 69-72: the four strongest brainstorm ideas for making the ring-t mark more its own.

69 Escape      the wave leaves the ring: motion is not held by the frame
70 Signature   the ring is one stroke that flies off into a swash at the gap
71 Drop        the wave's curl ends in a pen-lift drop
72 Echo        a hairline echo under the wave, like the original reference's double line
Run:  python3 build-69-72.py
"""
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import calligraphy as C  # noqa: E402
from calligraphy import INK, MINT_ON_WHITE as MINT, BRAND_MINT, ZAPF, taper, curl_from, wave_with_curl  # noqa: E402

WHITE = '#ffffff'
SET_TITLE = '69—72 · идеи из брейншторма: волна выходит за кольцо, кольцо-подпись, капля, эхо'
ON_DARK = {MINT: BRAND_MINT, INK: WHITE}
concepts = []


def add(slug, name, ru, idea, kind, body, on_dark=None, light_card=True):
    concepts.append({'slug': slug, 'name': name, 'ru': ru, 'idea': idea, 'type': kind,
                     'on_dark': on_dark or {}, 'light_card': light_card, 'set_title': SET_TITLE})
    (ROOT / 'svg' / f'{slug}.svg').write_text(C.master(f'Tatsi in motion — {name}', body))


def drop_at(p2, p3, r0, sweep_deg, shrink, r=5.5, fill=MINT):
    """A small dot just past the end of a ccw curl made by wave_with_curl(p2, p3, r0, sweep, shrink)."""
    phi = math.atan2(p3[1] - p2[1], p3[0] - p2[0])
    th0 = phi + math.pi / 2
    cx, cy = p3[0] - r0 * math.cos(th0), p3[1] - r0 * math.sin(th0)
    th_end = th0 - math.radians(sweep_deg)
    r_end = r0 * (1 - shrink)
    # a little further along the spiral so the dot sits just off the hairline end
    th_dot = th_end - math.radians(28)
    x, y = cx + (r_end + 1) * math.cos(th_dot), cy + (r_end + 1) * math.sin(th_dot)
    return f'<circle id="drop" cx="{C.fmt(x)}" cy="{C.fmt(y)}" r="{r}" fill="{fill}"/>'


def script_t(cx=256, cy=256, fill=MINT, dx=6, dy=-6):
    return C.placed(ZAPF, 't', C.size_for_height(ZAPF, 't', 270), cx, cy, fill=fill, pid='t', dx=dx, dy=dy)


# 69 — Escape: ring shifted left, the crossbar wave starts inside and exits past the ring with a curl outside
RING_C = (232, 256)
add('69-escape', 'Escape', 'Волна выходит за кольцо',
    'Волна-перекладина начинается внутри кольца и уходит за его край, заканчиваясь завитком снаружи: движение не удерживается рамкой.',
    'Идея · свобода', [
        C.ellipse_arc(*RING_C, 190, 190, -15, 290, width=6, color=MINT),
        wave_with_curl((90, 240), (170, 200), (300, 266), (486, 214), 8, 20, 330, 0.75, MINT, split=0.8),
        taper((180, 440), (250, 468), (326, 432), (410, 388), 6, fill=MINT, pid='wave-low'),
        script_t(*RING_C),
    ], ON_DARK)

# 70 — Signature: the ring is drawn in one stroke and flies off the gap in a swash
end_angle = 300
end = (256 + 200 * math.cos(math.radians(end_angle)), 256 + 200 * math.sin(math.radians(end_angle)))
end_phi = math.degrees(math.atan2(math.cos(math.radians(end_angle)), -math.sin(math.radians(end_angle))))
add('70-signature-ring', 'Signature ring', 'Кольцо-подпись',
    'Кольцо нарисовано одним движением и у разрыва вылетает наружу росчерком, как завершение подписи.',
    'Идея · росчерк', [
        C.brush_ring(256, 256, 200, -10, end_angle, 12, MINT, profile=lambda t: 0.45 + 0.55 * math.sin(math.pi * t) ** 1.2),
        curl_from(end, end_phi, 64, 95, 0.55, 6, MINT, pid='swash', ccw=False, steps=40),
        taper((84, 236), (170, 196), (300, 268), (468, 220), 8, fill=MINT, pid='wave'),
        script_t(),
    ], ON_DARK)

# 71 — Drop: curl on the wave tail ends in a small pen-lift drop
add('71-drop', 'Drop', 'Капля на завитке',
    'Петелька волны заканчивается маленькой каплей — след отрыва пера. Деталь заметна вблизи и не мешает издалека.',
    'Идея · деталь', [
        C.ellipse_arc(256, 256, 200, 200, -15, 290, width=6, color=MINT),
        wave_with_curl((84, 236), (170, 196), (300, 268), (468, 220), 8, 22, 300, 0.7, MINT),
        drop_at((300, 268), (468, 220), 22, 300, 0.7),
        taper((196, 448), (268, 478), (350, 440), (440, 392), 6, fill=MINT, pid='wave-low'),
        script_t(),
    ], ON_DARK)

# 72 — Echo: hairline echo line under the crossbar wave
add('72-echo', 'Echo', 'Эхо волны',
    'Под волной-перекладиной тонкая линия-эхо, как в первом референсе: ощущение движения в кадре без новых форм.',
    'Идея · эхо', [
        C.ellipse_arc(256, 256, 200, 200, -15, 290, width=6, color=MINT),
        taper((84, 236), (170, 196), (300, 268), (468, 220), 8, fill=MINT, pid='wave'),
        taper((120, 262), (190, 226), (300, 290), (430, 250), 3, fill=MINT, pid='wave-echo'),
        taper((196, 448), (268, 478), (350, 440), (440, 392), 6, fill=MINT, pid='wave-low'),
        script_t(),
    ], ON_DARK)

(ROOT / 'concepts-69-72.json').write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + '\n')
cards = ''.join(
    f'<div class="card"><img src="../svg/{c["slug"]}.svg"><div class="s"><img src="../svg/{c["slug"]}.svg" style="width:48px;height:48px"></div><div class="n">{c["slug"][:2]} · {c["name"]}</div></div>'
    for c in concepts)
(ROOT / 'preview' / 'variations-69-72.html').write_text(
    '<!doctype html><meta charset="utf-8"><title>69-72</title><style>body{margin:0;background:#e9eeeb;font:13px Helvetica,Arial;color:#3a4a47;padding:26px}'
    '.row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{border-radius:10px;padding:12px;background:#fff;border:1px solid #d8ddd9}'
    '.card img{width:100%;height:320px;object-fit:contain;display:block}.n{font-size:12px;margin-top:8px}.s{display:flex;gap:8px;align-items:flex-end;margin-top:6px;height:48px}</style>'
    f'<div class="row">{cards}</div>')
print(f'Built {len(concepts)} masters (69-72)')
