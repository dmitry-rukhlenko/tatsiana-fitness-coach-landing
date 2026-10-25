"""Check SVG fidelity, old-source preservation and both downloadable archives."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import posixpath
import re
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'
concepts=json.loads((ROOT/'concepts.json').read_text())
assert Counter(c['group'] for c in concepts)=={'A':7,'B':7,'C':7}

def geometry(svg):
    allowed=['g','path','circle','ellipse','rect','line','polygon','polyline']
    return [(e.tag,{k:v for k,v in e.attrib.items() if k!='id'}) for e in svg.iter() if e.tag.removeprefix(NS) in allowed]

placements=0
for c in concepts:
    filename=c['slug']+'.svg'
    main=ET.parse(ROOT/'svg'/filename).getroot()
    light=ET.parse(ROOT/'svg-light'/filename).getroot()
    for svg in [main,light]:
        assert not any(e.tag in [NS+t for t in ['text','image','script','foreignObject','use']] for e in svg.iter())
        assert all('href' not in k for e in svg.iter() for k in e.attrib)
        ids=[e.attrib['id'] for e in svg.iter() if 'id' in e.attrib]
        assert len(ids)==len(set(ids))
    colors={v for e in main.iter() for k,v in e.attrib.items() if k in ['fill','stroke'] and v!='none'}
    assert colors==({'#bcf7f3','#ffffff'} if c['group']=='B' else {'#bcf7f3'}),c['code']
    expected=[(tag,{k:'#142627' if v=='#ffffff' else v for k,v in attrs.items()}) for tag,attrs in geometry(main)]
    assert expected==geometry(light)
    symbols=re.findall(r'<svg\b.*?</svg>',(ROOT/'applications'/f"{c['slug']}.html").read_text(),re.S)
    assert len(symbols)==6
    for svg in symbols:
        assert geometry(ET.fromstring(svg))==geometry(main),c['code']
        placements+=1
    for folder in ['png','png-light']:
        png=(ROOT/folder/f"{c['slug']}.png").read_bytes()
        assert png[:8]==b'\x89PNG\r\n\x1a\n'
        width,height,depth,color=struct.unpack('>IIBB',png[16:26])
        assert (width,height,color)==(1024,1024,6)

baseline=json.loads((ROOT/'baseline-existing.json').read_text())
changed=[name for name,digest in baseline.items() if hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()!=digest]
assert not changed,changed
gallery=(ROOT/'applications.html').read_text()
assert gallery.count('role="tab"')==21 and gallery.count('role="tabpanel"')==21
assert gallery.count('role="tabpanel" aria-labelledby=')==21

files={}
for filename in ['index.html','applications.html','applications.js','README.md','concepts.json']:
    contents=(ROOT/filename).read_bytes()
    if filename.endswith('.html'):
        contents=contents.decode().replace('<a class="download" href="tatsi-refinements-21.zip" download>Скачать 21 вариант и все макеты ↓</a>','<a class="download" href="README.md">Состав набора и редактирование SVG ↗</a>').encode()
    files[filename]=contents
photos=set()
for folder in ['svg','svg-light','png','png-light','applications']:
    for file in sorted((ROOT/folder).iterdir()):
        contents=file.read_bytes()
        if file.suffix=='.html':
            source=contents.decode()
            photos.update(re.findall(r'src="\.\./\.\./\.\./images/([^"]+)"',source))
            contents=source.replace('../../../images/','../photos/').encode()
        files[file.relative_to(ROOT).as_posix()]=contents
for photo in photos:
    files['photos/'+photo]=(ROOT.parent.parent/'images'/photo).read_bytes()
for name in ['overview','group-a','group-b','group-c','small-sizes']:
    files['preview/'+name+'.png']=(ROOT/'preview'/f'{name}.png').read_bytes()
for filename,contents in files.items():
    if filename.endswith('.html'):
        for link in re.findall(r'(?:src|href)="([^"]+)"',contents.decode()):
            if link.startswith('#'):continue
            assert not re.match(r'^[a-z]+:',link),link
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(filename),link.split('#')[0]))
            assert resolved in files,(filename,link)

def archive(name,members):
    destination=ROOT/name
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for filename,contents in members.items():z.writestr(filename,contents)
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        assert all(z.read(filename)==contents for filename,contents in members.items())
    return dict(file=name,members=len(members),bytes=destination.stat().st_size,crc='pass')

full=archive('tatsi-refinements-21.zip',files)
vectors=archive('tatsi-refinements-svg.zip',{f:b for f,b in files.items() if f.endswith('.svg') or f=='README.md'})
report=dict(groups={'A':7,'B':7,'C':7},primary_svgs=21,light_svgs=21,
            transparent_pngs_1024=42,exact_geometry_placements=placements,
            preserved_source_files=len(baseline),changed_old_files=changed,
            broken_archive_links=0,archives=[full,vectors])
(ROOT/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
