"""Validate editable geometry and produce a self-contained handoff archive."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / 'logo-concepts-2026-10-25'
concepts = json.loads((ROOT / 'concepts-31-40.json').read_text())
NS = '{http://www.w3.org/2000/svg}'

def geometry(svg):
    return [{k: v for k, v in element.attrib.items() if k != 'id'} for element in svg.iter() if element.tag in [NS + t for t in ['path', 'circle', 'ellipse', 'rect', 'line', 'polygon', 'polyline']]]

placements = 0
for c in concepts:
    filename = c['slug'] + '.svg'
    main = ET.parse(ROOT / 'svg' / filename).getroot()
    light = ET.parse(ROOT / 'svg-light' / filename).getroot()
    for svg in [main, light]:
        assert not any(element.tag in [NS + t for t in ['text', 'image', 'script', 'foreignObject', 'use']] for element in svg.iter())
        assert all('href' not in k for element in svg.iter() for k in element.attrib)
        ids = [e.attrib['id'] for e in svg.iter() if 'id' in e.attrib]
        assert len(ids) == len(set(ids))
    assert {p['fill'] for p in geometry(main)} == {'#ffffff', '#bcf7f3'}
    assert {p['fill'] for p in geometry(light)} == {'#142627', '#bcf7f3'}
    assert [{**p, 'fill':'#142627' if p['fill'] == '#ffffff' else p['fill']} for p in geometry(main)] == geometry(light)
    symbols = re.findall(r'<svg\b.*?</svg>', (ROOT / 'applications' / (c['slug']+'.html')).read_text(), re.S)
    assert len(symbols) == 6
    for svg in symbols:
        assert geometry(ET.fromstring(svg)) == geometry(main), c['slug']
        placements += 1

baseline = json.loads((ROOT / 'baseline-existing.json').read_text())
changed = [f for f, digest in baseline.items() if hashlib.sha256((PREVIOUS / f).read_bytes()).hexdigest() != digest]
assert not changed, changed
gallery = (ROOT / 'applications.html').read_text()
shared = (PREVIOUS / 'applications.html').read_text()
assert len(re.findall(r'role="tabpanel"', gallery)) == 10
assert len(re.findall(r'role="tabpanel"', shared)) == 40
assert len(re.findall(r'role="tab"', shared)) == 40
assert len(re.findall(r'<section[^>]*role="tabpanel"[^>]*(?<!hidden)>', shared)) == 1

archive = ROOT / 'tatsi-in-motion-31-40.zip'
photos = set()
packed_files = {}
for filename in ['index.html', 'applications.html', 'applications.js', 'README.md']:
    contents = (ROOT / filename).read_bytes()
    if filename.endswith('.html'):
        text = contents.decode().replace('../logo-concepts-2026-10-25/index.html', 'preview/reference-31-40.png').replace('← Общая коллекция', '← Обзор всех десяти')
        text = text.replace('<a class="download" href="tatsi-in-motion-31-40.zip" download>Скачать 10 SVG и все макеты ↓</a>', '<a class="download" href="README.md">Состав набора и редактирование SVG ↗</a>')
        contents = text.encode()
    packed_files[filename] = contents
for folder in ['svg', 'svg-light', 'applications']:
    for file in sorted((ROOT / folder).iterdir()):
        contents = file.read_bytes()
        if file.suffix == '.html':
            text = contents.decode()
            photos.update(re.findall(r'src="\.\./\.\./\.\./images/([^"]+)"', text))
            contents = text.replace('../../../images/', '../photos/').encode()
        packed_files[file.relative_to(ROOT).as_posix()] = contents
for photo in photos:
    packed_files['photos/' + photo] = (ROOT.parent.parent / 'images' / photo).read_bytes()
packed_files['preview/reference-31-40.png'] = (ROOT / 'preview/reference-31-40.png').read_bytes()
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for filename, contents in packed_files.items():
        z.writestr(filename, contents)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert all(z.read(name) == contents for name, contents in packed_files.items())

report = dict(primary_svgs=10, light_svgs=10, exact_geometry_placements=placements,
              preserved_original_files=len(baseline), changed_original_files=changed,
              shared_tabs=40, shared_panels=40, archive_files=len(packed_files),
              archive_crc='pass', archive_bytes=archive.stat().st_size)
(ROOT / 'package-verification.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
