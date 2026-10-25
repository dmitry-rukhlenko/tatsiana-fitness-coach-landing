"""Build concepts 21-30: calligraphic / Didone direction (ink letterforms, thin mint flourishes) on white.

Letterforms are outlined from macOS system fonts with fontTools (glyphs.py) so the SVGs contain paths only.
Flourishes are tapered brush strokes built as filled shapes. Run:  python3 build-21-30.py
"""

from pathlib import Path
from html import escape
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import glyphs  # noqa: E402

INK = '#211D26'
# Brand mint #bcf7f3 is 1.2:1 against white (invisible for hairline flourishes); on white the same hue is used
# one step deeper. The gallery boards swap it back to #bcf7f3 on dark surfaces (see concepts-21-30.json).
MINT = '#86e3da'
BRAND_MINT = '#bcf7f3'
SNELL = ('SnellRoundhand.ttc', 1)   # Snell Roundhand Bold
ZAPF = ('Zapfino.ttf', 0)
DIDOT = ('Didot.ttc', 0)


def fmt(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def letters(font, text, size, x, y, fill=INK, tracking=0.0, pid='letters'):
    name, idx = font
    d, _ = glyphs.text_path(name, text, size, x, y, tracking=tracking, index=idx)
    return f'<path id="{pid}" d="{d}" fill="{fill}"/>'


def centered_x(font, text, size, cx, tracking=0.0):
    name, idx = font
    b = glyphs.text_bounds(name, text, size, 0, 0, tracking=tracking, index=idx)
    return cx - (b[0] + b[2]) / 2


def cubic(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0],
            mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1])


def cubic_tangent(p0, p1, p2, p3, t):
    mt = 1 - t
    return (3 * mt**2 * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t**2 * (p3[0] - p2[0]),
            3 * mt**2 * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t**2 * (p3[1] - p2[1]))


def taper(p0, p1, p2, p3, wmax, fill=MINT, pid='flourish', steps=28, profile=None):
    """A calligraphic stroke along a cubic: hairline ends, `wmax` thick in the middle, as one filled path."""
    profile = profile or (lambda t: math.sin(math.pi * t) ** 0.8)
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        x, y = cubic(p0, p1, p2, p3, t)
        tx, ty = cubic_tangent(p0, p1, p2, p3, t)
        n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        w = max(0.6, wmax * profile(t)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    d = 'M' + ' L'.join(f'{fmt(x)} {fmt(y)}' for x, y in pts) + ' Z'
    return f'<path id="{pid}" d="{d}" fill="{fill}"/>'


def ellipse_arc(cx, cy, rx, ry, a0, a1, rot_deg=0.0, width=6, color=MINT, pid='ring'):
    """Elliptical arc from angle a0 to a1 (degrees, parametric), rotated about the centre, as cubic Béziers."""
    rot = math.radians(rot_deg)
    cr, sr = math.cos(rot), math.sin(rot)

    def pt(x, y):
        return (cx + x * cr - y * sr, cy + x * sr + y * cr)

    a0, a1 = math.radians(a0), math.radians(a1)
    segs = max(1, math.ceil(abs(a1 - a0) / (math.pi / 2)))
    step = (a1 - a0) / segs
    k = 4 / 3 * math.tan(step / 4)
    parts = []
    for i in range(segs):
        t1, t2 = a0 + i * step, a0 + (i + 1) * step
        P0 = (rx * math.cos(t1), ry * math.sin(t1)); P3 = (rx * math.cos(t2), ry * math.sin(t2))
        P1 = (P0[0] - k * rx * math.sin(t1), P0[1] + k * ry * math.cos(t1))
        P2 = (P3[0] + k * rx * math.sin(t2), P3[1] - k * ry * math.cos(t2))
        if i == 0:
            x, y = pt(*P0); parts.append(f'M{fmt(x)} {fmt(y)}')
        a, b, c = pt(*P1), pt(*P2), pt(*P3)
        parts.append(f'C{fmt(a[0])} {fmt(a[1])} {fmt(b[0])} {fmt(b[1])} {fmt(c[0])} {fmt(c[1])}')
    return f'<path id="{pid}" d="{" ".join(parts)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'


def zapfino_ti(size, x, y):
    """Zapfino 'ti' in ink with the i-dot recoloured mint (the dot is the smallest closed contour of the i)."""
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    font = glyphs.load(*ZAPF)
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    scale = size / font['head'].unitsPerEm
    pen_x = 0.0
    ink_parts, dot = [], None
    for ch in 'ti':
        g = cmap[ord(ch)]
        rec = RecordingPen(); gs[g].draw(rec)
        # split the recording into contours
        contours, cur = [], []
        for op, args in rec.value:
            cur.append((op, args))
            if op in ('closePath', 'endPath'):
                contours.append(cur); cur = []
        for c in contours:
            tf = (scale, 0, 0, -scale, x + pen_x * scale, y)
            sp = SVGPathPen(gs); tp = TransformPen(sp, tf)
            bp = BoundsPen(gs); tb = TransformPen(bp, tf)
            for op, args in c:
                getattr(tp, op)(*args); getattr(tb, op)(*args)
            b = bp.bounds; area = (b[2] - b[0]) * (b[3] - b[1]) if b else 0
            item = (area, sp.getCommands())
            if ch == 'i' and (dot is None or area < dot[0]):
                if dot:
                    ink_parts.append(dot[1])
                dot = item
            else:
                ink_parts.append(item[1])
        pen_x += font['hmtx'][g][0]
    return (f'<path id="ti" d="{" ".join(ink_parts)}" fill="{INK}"/>', f'<path id="i-dot" d="{dot[1]}" fill="{MINT}"/>')


def master(slug, title, body, vb_w=512, vb_h=512):
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}" role="img" aria-labelledby="title">',
        f'  <title id="title">{escape(title)}</title>',
        f'  <!-- Letterforms outlined to paths (no fonts needed). Ink {INK}, deep mint {MINT} for white backgrounds; on dark surfaces use ink #ffffff and brand mint {BRAND_MINT}. -->',
        '  <g id="symbol">',
        *['    ' + part for part in body],
        '  </g>',
        '</svg>',
        '',
    ])


concepts = []


def add(slug, name, ru, idea, kind, body, vb=(512, 512)):
    concepts.append({'slug': slug, 'name': name, 'ru': ru, 'idea': idea, 'type': kind,
                     'on_dark': {INK: '#ffffff', MINT: BRAND_MINT}, 'light_card': True,
                     'set_title': '21—30 · третий набор: каллиграфия и антиква'})
    (ROOT / 'svg' / f'{slug}.svg').write_text(master(slug, f'Tatsi in motion — {name}', body, *vb))


# 21 — Zapfino t inside a thin open ring, a mint wave crossing the letter
x = centered_x(ZAPF, 't', 300, 256)
add('21-ring-script-t', 'Ring t', 'Росчерк t в кольце',
    'Каллиграфическая t внутри тонкого разомкнутого кольца; мятная волна проходит сквозь букву.', 'Каллиграфия · кольцо', [
        ellipse_arc(256, 256, 196, 196, -20, 300, width=7),
        taper((56, 268), (170, 226), (330, 312), (456, 258), 9, pid='wave'),
        letters(ZAPF, 't', 300, x, 394, pid='t'),
    ])

# 22 — Didone T with two ribbons weaving across the stem
x = centered_x(DIDOT, 'T', 440, 256)
add('22-didone-ribbon-t', 'Ribbon T', 'Антиквенная T с лентой',
    'Строгая антиквенная T, сквозь ножку которой проходят две тонкие мятные ленты — сила и пластика вместе.', 'Антиква · лента', [
        letters(DIDOT, 'T', 440, x, 412, pid='T'),
        taper((22, 178), (160, 118), (300, 236), (490, 150), 11, pid='ribbon-1'),
        taper((42, 208), (170, 162), (310, 256), (478, 186), 6, pid='ribbon-2'),
    ])

# 23 — Didone wordmark with a script mint "in"
d1, adv1 = glyphs.text_path(DIDOT[0], 'Tatsi ', 150, 44, 180, index=DIDOT[1])
d2, adv2 = glyphs.text_path(SNELL[0], 'in', 150, 44 + adv1, 180, index=SNELL[1])
d3, adv3 = glyphs.text_path(DIDOT[0], ' motion', 150, 44 + adv1 + adv2, 180, index=DIDOT[1])
right = 44 + adv1 + adv2 + adv3
add('23-didone-wordmark', 'Tatsi in motion', 'Антиквенное написание',
    'Полное имя антиквой; слово «in» написано мятным росчерком, а тонкий штрих под строкой задаёт движение.', 'Написание · антиква', [
        f'<path id="tatsi" d="{d1}" fill="{INK}"/>',
        f'<path id="in" d="{d2}" fill="{MINT}"/>',
        f'<path id="motion" d="{d3}" fill="{INK}"/>',
        taper((60, 214), (320, 240), (700, 198), (right - 30, 220), 7, pid='swash'),
    ], vb=(int(right + 44), 256))

# 24 — stacked lockup: ring + script t over spaced Didone caps
cap_tr = 220
cap_size = 38
x_t = centered_x(SNELL, 't', 300, 256)
x_c = centered_x(DIDOT, 'TATSI IN MOTION', cap_size, 256, tracking=cap_tr)
add('24-stacked-ring', 'Stacked ring', 'Кольцо и подпись',
    'Разомкнутое кольцо с рукописной t над разрядкой TATSI IN MOTION — классическая вертикальная композиция.', 'Эмблема · вертикаль', [
        ellipse_arc(256, 196, 150, 150, -20, 300, width=7),
        letters(SNELL, 't', 300, x_t, 267, pid='t'),
        letters(DIDOT, 'TATSI IN MOTION', cap_size, x_c, 458, tracking=cap_tr, pid='caption'),
    ])

# 25 — script "tatsi" with one mint swash through both t crossbars
x = centered_x(SNELL, 'tatsi', 230, 280)
add('25-script-tatsi', 'Script tatsi', 'Росчерк tatsi',
    'Рукописное tatsi одним дыханием; мятный росчерк проходит через перекладины обеих t.', 'Написание · росчерк', [
        letters(SNELL, 'tatsi', 230, x, 190, pid='tatsi'),
        taper((36, 126), (160, 96), (330, 150), (528, 108), 8, pid='swash'),
    ], vb=(560, 256))

# 26 — calligraphic Tm monogram: ink T, mint m, shared baseline
add('26-script-tm', 'Tm monogram', 'Монограмма Tm',
    'Каллиграфические инициалы: тёмная T и мятная m на одной базовой линии, росчерк T уходит под m.', 'Монограмма · каллиграфия', [
        letters(SNELL, 'm', 240, 290, 320, fill=MINT, pid='m'),
        letters(SNELL, 'T', 300, 10, 320, pid='T'),
    ])

# 27 — Didone stem with a mint wave as the crossbar
x = centered_x(DIDOT, 'I', 440, 256)
add('27-wave-crossbar-t', 'Wave crossbar', 'Волна-перекладина',
    'Антиквенная ножка T, а перекладину рисует мятная волна с тонким эхом — буква, которая двигается.', 'Антиква · волна', [
        letters(DIDOT, 'I', 440, x, 412, pid='stem'),
        taper((60, 114), (190, 70), (320, 152), (452, 104), 13, pid='wave'),
        taper((92, 142), (200, 108), (320, 174), (428, 138), 5, pid='echo'),
    ])

# 28 — Didone T inside a tilted open ellipse (orbit)
x = centered_x(DIDOT, 'T', 300, 256)
add('28-orbit-didone-t', 'Orbit T', 'Орбита T',
    'Антиквенная T внутри наклонённого разомкнутого эллипса — спокойный центр и траектория вокруг.', 'Антиква · орбита', [
        ellipse_arc(256, 256, 236, 158, 70, 370, rot_deg=-22, width=7),
        letters(DIDOT, 'T', 300, x, 362, pid='T'),
    ])

# 29 — Zapfino "ti" with a mint i-dot
x = centered_x(ZAPF, 'ti', 260, 256)
ti, dot = zapfino_ti(260, x, 376)
add('29-script-ti', 'Script ti', 'Росчерк ti',
    'Каллиграфическое ti (Tatsi in motion) с мятной точкой над i — лёгкий знак для аватара и печати.', 'Лигатура · каллиграфия', [ti, dot])

# 30 — large mint script T over spaced Didone caps
x_T = centered_x(SNELL, 'T', 340, 256)
x_c = centered_x(DIDOT, 'TATSI IN MOTION', cap_size, 256, tracking=cap_tr)
add('30-flourish-t', 'Flourish T', 'Росчерк T',
    'Крупная мятная каллиграфическая T с росчерком над разрядкой TATSI IN MOTION.', 'Каллиграфия · росчерк', [
        letters(SNELL, 'T', 340, x_T, 300, fill=MINT, pid='T'),
        letters(DIDOT, 'TATSI IN MOTION', cap_size, x_c, 422, tracking=cap_tr, pid='caption'),
    ])

(ROOT / 'concepts-21-30.json').write_text(json.dumps(concepts, ensure_ascii=False, indent=2) + '\n')

# White contact sheet for inspection (these marks are designed for light surfaces).
cards = ''.join(
    f'<div class="card"><div class="big"><img src="../svg/{c["slug"]}.svg"></div>'
    f'<div class="small"><img src="../svg/{c["slug"]}.svg" width="64" height="64"><img src="../svg/{c["slug"]}.svg" width="32" height="32"></div>'
    f'<div class="name">{c["slug"]}</div></div>' for c in concepts)
(ROOT / 'preview' / 'contact-sheet-21-30.html').write_text(f'''<!doctype html><meta charset="utf-8"><title>21-30</title>
<style>body{{margin:0;background:#f3f1ee;font:13px Helvetica,Arial;color:#555;padding:28px}}.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:18px}}
.card{{background:#fff;border-radius:10px;padding:14px;border:1px solid #e3e0da}}.big img{{width:100%;height:220px;object-fit:contain;display:block}}
.small{{display:flex;gap:12px;align-items:flex-end;height:64px;margin:10px 0 6px}}.name{{font-size:11px;color:#999}}</style>
<div class="grid">{cards}</div>''')
print(f'Built {len(concepts)} masters (21-30) and concepts-21-30.json')
