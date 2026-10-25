"""Outline text from a macOS font into SVG path data (fontTools; no <text> in the output)."""
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_DIR = '/System/Library/Fonts/Supplemental/'
_cache = {}


def load(name, index=0):
    key = (name, index)
    if key not in _cache:
        path = FONT_DIR + name
        font = TTCollection(path).fonts[index] if path.endswith('.ttc') else TTFont(path)
        _cache[key] = font
    return _cache[key]


def font_names(name):
    """List the faces inside a .ttc so the right style index can be picked."""
    path = FONT_DIR + name
    fonts = TTCollection(path).fonts if path.endswith('.ttc') else [TTFont(path)]
    return [f['name'].getDebugName(4) for f in fonts]


def text_path(name, text, size, x=0.0, y=0.0, tracking=0.0, index=0, kern=True):
    """Return (d, advance_width) for `text` with the baseline at y and the left edge at x (SVG y-down)."""
    font = load(name, index)
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    upem = font['head'].unitsPerEm
    scale = size / upem
    hmtx = font['hmtx']
    kern_pairs = {}
    if kern and 'kern' in font:
        for table in font['kern'].kernTables:
            kern_pairs.update(getattr(table, 'kernTable', {}))
    names = [cmap.get(ord(ch), '.notdef') for ch in text]
    d_parts = []
    pen_x = 0.0
    for i, gname in enumerate(names):
        if i and kern_pairs:
            pen_x += kern_pairs.get((names[i - 1], gname), 0)
        pen = SVGPathPen(glyph_set)
        # font units -> SVG: scale, flip y, then translate to the pen position
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x + pen_x * scale, y))
        glyph_set[gname].draw(tpen)
        d = pen.getCommands()
        if d:
            d_parts.append(d)
        pen_x += hmtx[gname][0] + tracking
    return ' '.join(d_parts), pen_x * scale


def text_bounds(name, text, size, x=0.0, y=0.0, tracking=0.0, index=0):
    font = load(name, index)
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    upem = font['head'].unitsPerEm
    scale = size / upem
    hmtx = font['hmtx']
    pen_x = 0.0
    box = None
    for ch in text:
        gname = cmap.get(ord(ch), '.notdef')
        bp = BoundsPen(glyph_set)
        glyph_set[gname].draw(TransformPen(bp, (scale, 0, 0, -scale, x + pen_x * scale, y)))
        if bp.bounds:
            b = bp.bounds
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        pen_x += hmtx[gname][0] + tracking
    return box
