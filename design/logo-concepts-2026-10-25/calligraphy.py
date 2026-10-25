"""Shared helpers for the calligraphic sets: outlined letterforms, tapered brush strokes, open rings.

Used by build-41-61.py (build-21-30.py keeps its own copy of the same helpers).
"""
from html import escape
import math

import glyphs

INK = '#211D26'
MINT_ON_WHITE = '#86e3da'   # brand hue one step deeper, readable on white
BRAND_MINT = '#bcf7f3'      # the brand mint, for dark surfaces

SNELL = ('SnellRoundhand.ttc', 1)      # Snell Roundhand Bold
SNELL_LIGHT = ('SnellRoundhand.ttc', 0)
ZAPF = ('Zapfino.ttf', 0)
SAVOYE = ('Savoye LET.ttc', 0)
CHANCERY = ('Apple Chancery.ttf', 0)
DIDOT = ('Didot.ttc', 0)


def fmt(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def letters(font, text, size, x, y, fill=INK, tracking=0.0, pid='letters'):
    name, idx = font
    d, _ = glyphs.text_path(name, text, size, x, y, tracking=tracking, index=idx)
    return f'<path id="{pid}" d="{d}" fill="{fill}"/>'


def bounds(font, text, size, tracking=0.0):
    name, idx = font
    return glyphs.text_bounds(name, text, size, 0, 0, tracking=tracking, index=idx)


def size_for_height(font, text, height):
    b = bounds(font, text, 100)
    return 100 * height / (b[3] - b[1])


def placed(font, text, size, cx, cy, fill=INK, pid='letters', dx=0.0, dy=0.0):
    """Letters whose bounding box is centred on (cx, cy), with an optional optical nudge."""
    b = bounds(font, text, size)
    x = cx - (b[0] + b[2]) / 2 + dx
    y = cy - (b[1] + b[3]) / 2 + dy
    return letters(font, text, size, x, y, fill=fill, pid=pid)


def cubic(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0],
            mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1])


def taper_fn(fn, wmax, profile, fill, pid, steps=40, t0=0.0, t1=1.0):
    """Variable-width stroke along fn(t) -> (x, y): one filled outline, tangent taken numerically."""
    left, right = [], []
    for i in range(steps + 1):
        t = t0 + (t1 - t0) * i / steps
        x, y = fn(t)
        xa, ya = fn(max(t0, t - 1e-3)); xb, yb = fn(min(t1, t + 1e-3))
        tx, ty = xb - xa, yb - ya
        n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        w = max(0.5, wmax * profile((t - t0) / (t1 - t0))) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    d = 'M' + ' L'.join(f'{fmt(x)} {fmt(y)}' for x, y in pts) + ' Z'
    return f'<path id="{pid}" d="{d}" fill="{fill}"/>'


def sine_profile(t):
    return math.sin(math.pi * t) ** 0.8


def taper(p0, p1, p2, p3, wmax, fill=MINT_ON_WHITE, pid='flourish', profile=None, steps=36):
    return taper_fn(lambda t: cubic(p0, p1, p2, p3, t), wmax, profile or sine_profile, fill, pid, steps)


def brush_ring(cx, cy, r, a0, a1, wmax, fill, pid='ring', profile=None, steps=90):
    """A ring drawn with a brush: thickness follows `profile` along the arc from angle a0 to a1 (degrees)."""
    a0r, a1r = math.radians(a0), math.radians(a1)

    def fn(t):
        a = a0r + (a1r - a0r) * t
        return (cx + r * math.cos(a), cy + r * math.sin(a))
    return taper_fn(fn, wmax, profile or (lambda t: 0.55 + 0.45 * math.sin(math.pi * t)), fill, pid, steps)


def ellipse_arc(cx, cy, rx, ry, a0, a1, rot_deg=0.0, width=6, color=MINT_ON_WHITE, pid='ring'):
    """Elliptical arc as cubic Béziers (uniform stroke), rotated about its centre."""
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


def master(title, body, vb_w=512, vb_h=512, note=''):
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}" role="img" aria-labelledby="title">',
        f'  <title id="title">{escape(title)}</title>',
        f'  <!-- {note} Letterforms are outlined paths; no fonts needed. -->' if note else '  <!-- Letterforms are outlined paths; no fonts needed. -->',
        '  <g id="symbol">',
        *['    ' + part for part in body],
        '  </g>',
        '</svg>',
        '',
    ])
