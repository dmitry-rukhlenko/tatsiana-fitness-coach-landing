"""Add a further set of concepts to the existing galleries and build their placement mockups.

Same board template as build-applications.py; the first ten concepts and their files are not touched.
Run from any directory:
  python3 build-applications-11-20.py                          # concepts-11-20.json: boards + gallery pages
  python3 build-applications-11-20.py concepts-21-30.json      # any other set
  python3 build-applications-11-20.py [concepts.json] --zip    # after render: refresh both ZIP archives
Optional per-concept keys: "on_dark" {colour: colour} swaps paint for the dark mockup surfaces,
"light_card" true gives the gallery card a white art area, "set_title" labels the set's divider.
"""

from pathlib import Path
from html import escape
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'applications'
SKILL_SCRIPTS = Path.home() / '.claude' / 'skills' / 'logo-design' / 'scripts'
sys.path.insert(0, str(SKILL_SCRIPTS))
import svglib  # noqa: E402  (bundled with the logo-design skill; pure Python)

CONCEPTS_FILE = next((a for a in sys.argv[1:] if a.endswith('.json')), 'concepts-11-20.json')
concepts = json.loads((ROOT / CONCEPTS_FILE).read_text())
FIRST, LAST = int(concepts[0]['slug'][:2]), int(concepts[-1]['slug'][:2])
# Total number of concepts across every set present in the folder (for "N of M" labels).
TOTAL = max(int(p.name[:2]) for p in (ROOT / 'svg').glob('[0-9][0-9]-*.svg'))
SET_TITLE = concepts[0].get('set_title', f'{FIRST:02d}—{LAST:02d}')
SVG_NS = '{http://www.w3.org/2000/svg}'


def stroke_half_width(el, parents):
    """Half of the effective stroke width (inherited through <g>), 0 for fills."""
    node = el
    while node is not None:
        if node.get('stroke') == 'none':
            return 0.0
        width = node.get('stroke-width')
        if width is not None:
            return float(width) / 2
        node = parents.get(node)
    return 0.0


def painted_bounds(path):
    """Tight bbox of the artwork including stroke caps (the master viewBox is larger than the mark)."""
    root = ET.parse(path).getroot()
    parents = {c: p for p in root.iter() for c in p}
    bbox = None
    for el, m in svglib.iter_shapes(root):
        pts = []
        for sp in svglib.shape_to_subpaths(el):
            for seg in sp:
                pts.extend(svglib.apply(m, p) for p in svglib.segment_points(seg))
        bb = svglib.bbox_of(pts)
        if not bb:
            continue
        half = stroke_half_width(el, parents)
        bb = (bb[0] - half, bb[1] - half, bb[2] + half, bb[3] + half)
        bbox = svglib.union_bbox(bbox, bb)
    x0, y0, x1, y1 = bbox
    return {'x': x0, 'y': y0, 'width': x1 - x0, 'height': y1 - y0}


def mark(concept, suffix):
    """Inline copy of the master, cropped to the mark, with ids made unique for the page."""
    svg = (ROOT / 'svg' / (concept['slug'] + '.svg')).read_text()
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    b = concept['bounds']
    pad = 10
    viewbox = f"{b['x']-pad:.2f} {b['y']-pad:.2f} {b['width']+2*pad:.2f} {b['height']+2*pad:.2f}"
    svg = re.sub(r'viewBox="[^"]*"', f'viewBox="{viewbox}"', svg, count=1)
    svg = re.sub(r'\swidth="\d+" height="\d+"', '', svg, count=1)
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{suffix}-{m[1]}"', svg)
    svg = svg.replace('aria-labelledby="title"', f'aria-labelledby="{suffix}-title"')
    # Every mockup surface is dark: marks drawn for white paper swap their paints here.
    for src, dst in concept.get('on_dark', {}).items():
        svg = re.sub(re.escape(src), dst, svg, flags=re.IGNORECASE)
    return svg


def site_brand(c):
    logo = mark(c, 'site')
    if c['slug'] == '16-tatsi-wave':
        return f'<div class="wordmark-brand">{logo}<span>in motion</span></div>'
    if c['slug'] == '23-didone-wordmark':
        return f'<div class="wordmark-brand motion">{logo}</div>'
    if c['slug'] == '25-script-tatsi':
        return f'<div class="wordmark-brand">{logo}<span>in motion</span></div>'
    if c['slug'] in ('24-stacked-ring', '30-flourish-t'):
        return f'<div class="site-brand"><div class="site-logo" style="width:66px;height:66px">{logo}</div></div>'
    return f'<div class="site-brand"><div class="site-logo">{logo}</div><span>Tatsi <small>in motion</small></span></div>'


# Identical to build-applications.py so the twenty boards look the same.
CSS = '''
*{box-sizing:border-box}body{margin:0;background:#e9eeeb;color:#192b29;font-family:Arial,Helvetica,sans-serif}.board{width:1600px;min-height:1100px;padding:45px 52px 35px}.board-heading{display:flex;justify-content:space-between;gap:30px;align-items:center;margin-bottom:35px}.heading-left{display:flex;align-items:center;gap:22px}.hero-mark{width:84px;height:84px;border-radius:20px;background:#142627;display:flex;align-items:center;justify-content:center;padding:17px}.hero-mark svg{width:100%;height:100%}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#61746b;margin:0 0 10px}.board h1{font-size:34px;font-weight:500;letter-spacing:-.03em;margin:0}.concept-note{font-size:13px;color:#61746b;max-width:390px;line-height:1.5;margin:0}.applications{display:grid;grid-template-columns:1040px 420px;gap:36px;align-items:start}.application-label{font-size:12px;letter-spacing:.08em;margin:0 0 14px;text-transform:uppercase;color:#61746b}.website{width:1040px;height:730px;background:#faf7f2;border-radius:12px;overflow:hidden;border:1px solid #d4dbd6}.browser-bar{height:36px;display:flex;align-items:center;padding:0 16px;background:#f2f4f0;border-bottom:1px solid #d4dbd6}.browser-dots{display:flex;gap:6px}.browser-dots i{width:7px;height:7px;border-radius:50%;background:#bdc8c1}.browser-title{font-size:10px;letter-spacing:.06em;margin:auto;color:#7a8b80}.website-nav{height:94px;background:#142627;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 36px;gap:18px}.site-brand{display:flex;align-items:center;gap:13px;min-width:225px}.site-logo{width:51px;height:55px}.site-logo svg{width:100%;height:100%}.site-brand>span{font-size:24px;letter-spacing:-.04em}.site-brand small{display:block;font-size:11px;letter-spacing:.08em;margin-top:3px}.wordmark-brand{width:170px;height:66px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:5px}.wordmark-brand svg{width:126px;height:40px}.wordmark-brand>span{font-size:10px;letter-spacing:.17em;margin-left:3px}.wordmark-brand.motion{gap:4px}.wordmark-brand.motion svg{width:140px;height:29px}.nav-items{display:flex;align-items:center;gap:24px;font-size:12px;color:#e5efeb}.site-cta{font-size:11px;background:#bcf7f3;color:#142627;padding:13px 17px;border-radius:5px}.site-hero{height:525px;display:grid;grid-template-columns:1.25fr .9fr;gap:35px;padding:38px 36px 30px}.hero-copy{padding-top:25px}.site-kicker{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#597368;margin:0 0 22px}.site-hero h2{font-size:47px;line-height:1.09;font-weight:400;letter-spacing:-.05em;margin:0 0 22px}.site-hero h2 span{display:block}.site-hero h2 em{font-style:normal;color:#6a8c81}.site-lead{font-size:13px;line-height:1.65;color:#627369;max-width:420px}.site-actions{display:flex;gap:13px;margin-top:28px;align-items:center;font-size:12px}.site-actions .primary{background:#142627;color:#fff;padding:15px 20px;border-radius:5px}.site-actions .secondary{padding:13px 9px;color:#3e594f}.hero-photo{height:457px;overflow:hidden;border-radius:90px 12px 12px 12px}.hero-photo img{width:100%;height:100%;object-fit:cover;object-position:center 45%}.site-footer-strip{margin:0 36px;display:flex;gap:20px;padding-top:18px;border-top:1px solid #d8dfd8;font-size:11px;color:#61746b}.site-footer-strip span+span:before{content:'·';margin-right:20px;color:#76958a}.website-notes{margin-top:24px;display:grid;grid-template-columns:1fr 1fr;gap:35px;color:#61746b;font-size:12px;line-height:1.6}.website-notes p{margin:0}.website-notes strong{font-weight:500;color:#243c32;display:block;margin-bottom:6px}.instagram{width:420px;height:812px;border-radius:28px;background:#fff;border:1px solid #d2d9d5;color:#111;overflow:hidden;position:relative}.phone-status{display:flex;justify-content:space-between;font-size:11px;font-weight:bold;height:38px;padding:14px 25px 5px}.instagram-top{height:46px;display:flex;justify-content:space-between;align-items:center;padding:0 21px;font-size:17px;font-weight:bold}.ig-top-icons{font-size:23px;font-weight:400;letter-spacing:10px}.profile-head{display:flex;align-items:center;gap:22px;padding:13px 21px 16px}.avatar-ring{flex-shrink:0;width:88px;height:88px;border-radius:50%;border:2px solid #bcf7f3;padding:4px}.avatar{width:100%;height:100%;border-radius:50%;background:#142627;display:flex;align-items:center;justify-content:center;padding:15px}.avatar svg{width:100%;height:100%}.profile-stats{display:flex;justify-content:space-between;flex:1;gap:15px;text-align:center;font-size:10px}.profile-stats b{display:block;font-size:19px;font-weight:600;margin-bottom:5px}.profile-bio{padding:0 23px;font-size:12px;line-height:1.55}.profile-bio b{display:block;font-weight:600}.profile-bio .category{color:#8b8b8b;font-size:11px}.bio-link{color:#193e61;font-weight:bold;margin-top:4px}.ig-actions{display:flex;gap:7px;margin:14px 21px 16px}.ig-actions span{flex:1;text-align:center;padding:8px;border-radius:6px;font-size:11px;background:#efefef;font-weight:bold}.ig-actions .follow{background:#4197f5;color:#fff}.highlights{display:flex;gap:23px;padding:0 24px 16px}.highlight{text-align:center;font-size:9px}.highlight i{width:49px;height:49px;border:1px solid #d9dfda;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:17px;color:#3d5f53;background:#edf5f1;margin-bottom:5px}.highlight:nth-child(2) i{background:#e5f7f4}.highlight:nth-child(3) i{background:#f2e9ef}.tabs{height:38px;border-top:1px solid #eee;display:flex;justify-content:space-around;align-items:center;color:#8d8d8d}.tabs span{font-size:21px}.tabs span:first-child{color:#111}.post-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}.post-grid>div{height:159px;position:relative;overflow:hidden}.post-grid img{width:100%;height:100%;object-fit:cover;object-position:50% 44%}.post-grid .post-brand{background:#142627;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:13px;color:#fff;text-align:center}.post-brand .post-mark{width:64px;height:65px}.post-mark svg{width:100%;height:100%}.post-brand p{font-size:15px;line-height:1.1;letter-spacing:-.04em;margin:0}.post-brand small{font-size:6px;letter-spacing:.14em;color:#bcf7f3}.post-grid .mint-post{background:#bcf7f3;color:#19372f;display:flex;align-items:center;justify-content:center;text-align:left;font-size:24px;line-height:1.08;letter-spacing:-.04em}.photo-logo{position:absolute;bottom:9px;right:9px;width:29px;height:29px;background:#142627;border-radius:50%;padding:6px}.photo-logo svg{width:100%;height:100%}.ig-bottom{position:absolute;bottom:0;left:0;right:0;height:40px;display:flex;align-items:center;justify-content:space-around;background:white;border-top:1px solid #eee;font-size:22px}.mini-avatar{width:22px;height:22px;background:#142627;border-radius:50%;padding:5px}.mini-avatar svg{width:100%;height:100%}.social-note{font-size:11px;line-height:1.55;color:#61746b;margin:16px 0 0}.board-footer{margin-top:25px;padding-top:17px;border-top:1px solid #d1dad3;display:flex;justify-content:space-between;color:#61746b;font-size:11px;line-height:1.5}
'''


def build_boards():
    OUT.mkdir(exist_ok=True)
    for c in concepts:
        c['bounds'] = painted_bounds(ROOT / 'svg' / (c['slug'] + '.svg'))
    for c in concepts:
        i = int(c['slug'][:2])
        hero_logo, avatar_logo, post_logo, photo_logo, mini_logo = (mark(c, s) for s in ('hero', 'avatar', 'post', 'photo', 'mini'))
        website = f'''<div class="website" id="website-preview">
      <div class="browser-bar"><span class="browser-dots"><i></i><i></i><i></i></span><span class="browser-title">TATSI IN MOTION · WEBSITE PREVIEW</span></div>
      <div class="website-nav">{site_brand(c)}<div class="nav-items"><span>Für wen</span><span>Coaching</span><span>Über mich</span><span>DE / EN</span><span class="site-cta">Kostenlose Beratung ↗</span></div></div>
      <div class="site-hero"><div class="hero-copy"><p class="site-kicker">Mobility &amp; Fitness Coaching</p><h2><span>Freier bewegen.</span><span>Stärker trainieren.</span><span><em>Besser fühlen.</em></span></h2><p class="site-lead">Kostenlose Online-Beratung für Erwachsene, die mehr Bewegungsfreiheit, bessere Haltung und ein Training suchen, das wirklich in den Alltag passt.</p><div class="site-actions"><span class="primary">Beratung anfragen ↗</span><span class="secondary">So läuft es ab</span></div></div><div class="hero-photo"><img src="../../../images/tatsiana-hero.jpg" alt="Татьяна на фотографии с сайта"></div></div>
      <div class="site-footer-strip"><span>Mobility first</span><span>Beweglichkeit &amp; Körperkontrolle</span><span>Persönliches Online-Coaching</span></div>
    </div>'''
        instagram = f'''<div class="instagram" id="instagram-preview">
      <div class="phone-status"><span>9:41</span><span>▮▮▮ &nbsp; ◔ &nbsp; ▰</span></div>
      <div class="instagram-top"><span>tatsi.in.motion⌄</span><span class="ig-top-icons">⊞ ≡</span></div>
      <div class="profile-head"><div class="avatar-ring"><div class="avatar">{avatar_logo}</div></div><div class="profile-stats"><span><b>—</b>posts</span><span><b>—</b>followers</span><span><b>—</b>following</span></div></div>
      <div class="profile-bio"><b>Tatsi in motion | Fitness coaching</b><span class="category">Fitness Trainer</span><div>Move freely. Feel strong.<br>Mobility · strength · body awareness</div><div class="bio-link">Free online consultation ↗</div></div>
      <div class="ig-actions"><span class="follow">Follow</span><span>Message</span><span>Contact</span></div>
      <div class="highlights"><div class="highlight"><i>↗</i>Start here</div><div class="highlight"><i>∿</i>Mobility</div><div class="highlight"><i>+</i>Coaching</div></div>
      <div class="tabs"><span>▦</span><span>▷</span><span>▣</span></div>
      <div class="post-grid"><div><img src="../../../images/tatsiana-hero.jpg" alt="Пример фотопубликации"></div><div class="post-brand"><div class="post-mark">{post_logo}</div><p>Move freely.</p><small>TATSI IN MOTION</small></div><div><img src="../../../images/tatsiana-mobility.jpg" alt="Пример фотографии с логотипом"><span class="photo-logo">{photo_logo}</span></div><div><img src="../../../images/tatsiana-about-handstand.jpg" alt="Фотография стойки на руках с сайта"></div><div class="mint-post">Strong.<br>Mobile.<br>You.</div><div><img src="../../../images/tatsiana-offer.jpg" alt="Фотография тренера с сайта"></div></div>
      <div class="ig-bottom"><span>⌂</span><span>⌕</span><span>⊞</span><span>▷</span><span class="mini-avatar">{mini_logo}</span></div>
    </div>'''
        html = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{i:02d} · {escape(c['name'])} — сайт и Instagram</title><style>{CSS}</style></head><body><main class="board">
    <header class="board-heading"><div class="heading-left"><div class="hero-mark">{hero_logo}</div><div><p class="eyebrow">Tatsi in motion / {i:02d} of {TOTAL}</p><h1>{escape(c['name'])}</h1></div></div><p class="concept-note">{escape(c['idea'])}</p></header>
    <div class="applications"><section><p class="application-label">01 / Сайт · шапка и первый экран</p>{website}<div class="website-notes"><p><strong>Белый + #bcf7f3</strong>Тёмная шапка даёт контраст светлому логотипу. В макете использованы фотография и тексты существующего сайта.</p><p><strong>Один знак в разных размерах</strong>Геометрия и цвета совпадают с SVG. Здесь скорректированы только размер и свободное поле вокруг знака.</p></div></section><section><p class="application-label">02 / Instagram · аватар и публикации</p>{instagram}<p class="social-note">Макет профиля. Имя пользователя — пример; показатели не указаны. Публикации иллюстрируют оформление.</p></section></div>
    <footer class="board-footer"><span>Вариант {i:02d} · {escape(c['ru'])} · локальная примерка логотипа</span><span>SVG сохранён отдельно · 25.10.2026</span></footer>
    </main></body></html>'''
        (OUT / (c['slug'] + '.html')).write_text(html)
    print(f'Built {len(concepts)} boards ({FIRST:02d}-{LAST:02d}).')


def extend_applications_page():
    path = ROOT / 'applications.html'
    page = path.read_text()
    if f'id="tab-{FIRST:02d}"' in page:
        print(f'applications.html already has tabs {FIRST:02d}-{LAST:02d}.')
        return
    tabs = ''.join(
        f'<a href="#concept-{i:02d}" id="tab-{i:02d}" role="tab" aria-controls="panel-{i:02d}" aria-selected="false" tabindex="-1">{i:02d}</a>'
        for i in range(FIRST, LAST + 1))
    sections = []
    for c in concepts:
        i = int(c['slug'][:2]); slug = c['slug']
        sections.append(f'''<section id="panel-{i:02d}" role="tabpanel" aria-labelledby="tab-{i:02d}" tabindex="0" hidden><div class="section-title"><h2>{i:02d} / {escape(c['name'])}</h2><a href="svg/{slug}.svg" download>Скачать SVG ↓</a></div><a href="applications/{slug}-board.png" target="_blank"><img src="applications/{slug}-board.png" alt="{escape(c['name'])}: пример на сайте и в Instagram" loading="eager" width="1600" height="1200"></a><div class="links"><a href="applications/{slug}-website.png" target="_blank">Сайт отдельно ↗</a><a href="applications/{slug}-instagram.png" target="_blank">Instagram отдельно ↗</a><a href="applications/{slug}.html" target="_blank">Макет HTML ↗</a></div></section>''')
    page = page.replace('</nav>', tabs + '</nav>', 1)
    page = page.replace('</main>', '\n'.join(sections) + '</main>', 1)
    if FIRST == 11:
        page = page.replace('Наведите мышку на номер', 'Варианты 01–10 — первый набор, 11–20 — второй (геометрический). Наведите мышку на номер', 1)
    else:
        label = SET_TITLE.split('·', 1)[-1].strip().rstrip('.')
        page = page.replace('. Наведите мышку на номер', f', {FIRST}–{LAST} — {label}. Наведите мышку на номер', 1)
    path.write_text(page)
    print(f'applications.html extended with tabs {FIRST:02d}-{LAST:02d}.')


def extend_index_page():
    path = ROOT / 'index.html'
    page = path.read_text()
    if f'id="concept-{FIRST:02d}"' in page:
        print(f'index.html already has cards {FIRST:02d}-{LAST:02d}.')
        return
    divider = SET_TITLE if FIRST != 11 else '11—20 · второй набор: геометрические знаки'
    cards = [f'<h2 class="set-divider" style="grid-column:1/-1;margin:26px 0 4px;font-size:14px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#bcf7f3">{escape(divider)}</h2>']
    for c in concepts:
        i = int(c['slug'][:2])
        art_style = ' style="background:#fff;border-radius:6px;padding:14px"' if c.get('light_card') else ''
        cards.append(f'''<article class="concept" id="concept-{i:02d}">
      <div class="card-top"><span class="number">{i:02d}</span><span>{escape(c['type'])}</span></div>
      <div class="art"{art_style}><img src="svg/{c['slug']}.svg" alt="{escape(c['ru'])}" width="512" height="512"></div>
      <div class="card-bottom"><div><h2>{escape(c['name'])}</h2><p class="ru">{escape(c['ru'])}</p></div><a href="svg/{c['slug']}.svg" download aria-label="Скачать {escape(c['name'])} в SVG">SVG <span aria-hidden="true">↓</span></a></div>
      <p class="rationale">{escape(c['idea'])}</p><p style="margin:14px 0 0;font-size:12px"><a href="applications.html#concept-{i:02d}" style="color:#bcf7f3;text-decoration:none">Сайт + Instagram →</a></p>
    </article>''')
    page = page.replace('</article></section>', '</article>\n' + '\n'.join(cards) + '</section>', 1)
    page = re.sub(r'Logo exploration / 01—\d+', f'Logo exploration / 01—{LAST}', page, count=1)
    page = re.sub(r'<title>Tatsi in motion — \d+ logo concepts</title>', f'<title>Tatsi in motion — {LAST} logo concepts</title>', page, count=1)
    page = re.sub(r'(Десять разных знаков|[А-Яа-яЁё\d]+ знак(?:ов|а)? в [А-Яа-яЁё]+ наборах) для выбора направления\.',
                  f'{LAST} знаков в нескольких наборах для выбора направления.', page, count=1)
    page = re.sub(r'Скачать \d+ SVG ↓', f'Скачать {LAST} SVG ↓', page, count=1)
    page = re.sub(r'aria-label="[^"]* вариантов логотипа"', f'aria-label="{LAST} вариантов логотипа"', page, count=1)
    page = re.sub(r'Посмотреть все \d+ вариантов', f'Посмотреть все {LAST} вариантов', page, count=1)
    path.write_text(page)
    print(f'index.html extended with cards {FIRST:02d}-{LAST:02d}.')


def refresh_zips():
    """Add the 11-20 files to both archives; existing entries for 01-10 are kept byte for byte."""
    with zipfile.ZipFile(ROOT / 'tatsi-in-motion-10-svg.zip', 'a', zipfile.ZIP_DEFLATED) as archive:
        names = set(archive.namelist())
        for c in concepts:
            arc = f'tatsi-in-motion/{c["slug"]}.svg'
            if arc not in names:
                archive.write(ROOT / 'svg' / (c['slug'] + '.svg'), arc)
    if '--svg-only' in sys.argv:
        # The preview pack is already ~70 MB; GitHub refuses files over 100 MB, so later sets add SVGs only.
        print('ZIP: SVG archive refreshed; preview pack left unchanged (--svg-only).')
        return
    with zipfile.ZipFile(ROOT / 'tatsi-in-motion-preview-pack.zip', 'a', zipfile.ZIP_DEFLATED) as archive:
        names = set(archive.namelist())
        for c in concepts:
            for kind in ('board', 'website', 'instagram'):
                arc = f'tatsi-in-motion/{c["slug"]}/{kind}.png'
                src = OUT / f'{c["slug"]}-{kind}.png'
                if arc not in names and src.exists():
                    archive.write(src, arc)
            arc = f'tatsi-in-motion/{c["slug"]}/{c["slug"]}.svg'
            if arc not in names:
                archive.write(ROOT / 'svg' / (c['slug'] + '.svg'), arc)
    print(f'ZIP archives refreshed with {FIRST:02d}-{LAST:02d}.')


if __name__ == '__main__':
    if '--zip' in sys.argv:
        refresh_zips()
    else:
        build_boards()
        extend_applications_page()
        extend_index_page()
