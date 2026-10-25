"""Build local placement mockups; do not modify the website or social accounts."""

from pathlib import Path
import json
import re
from html import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'applications'
OUT.mkdir(exist_ok=True)
concepts = json.loads((ROOT / 'concepts.json').read_text())
bounds = {row['file']: row for row in json.loads((ROOT / 'verification.json').read_text())['browser']['geometry_bounds']}


def mark(concept, suffix):
    filename = concept['slug'] + '.svg'
    svg = (ROOT / 'svg' / filename).read_text()
    svg = re.sub(r'<\?xml[^>]*>\s*', '', svg)
    b = bounds[filename]
    pad = 20
    viewbox = f"{b['x']-pad:.2f} {b['y']-pad:.2f} {b['width']+2*pad:.2f} {b['height']+2*pad:.2f}"
    svg = svg.replace('viewBox="0 0 512 512"', f'viewBox="{viewbox}"')
    svg = svg.replace('width="512" height="512"', '')
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{suffix}-{m[1]}"', svg)
    svg = svg.replace('aria-labelledby="logo-title logo-description"', f'aria-labelledby="{suffix}-logo-title {suffix}-logo-description"')
    return svg


def site_brand(c):
    logo = mark(c, 'site')
    if c['slug'].startswith('06'):
        return f'<div class="wordmark-brand">{logo}<span>in motion</span></div>'
    if c['slug'].startswith('09'):
        return f'<div class="wordmark-brand motion"><span>tatsi in</span>{logo}</div>'
    return f'<div class="site-brand"><div class="site-logo">{logo}</div><span>Tatsi <small>in motion</small></span></div>'


CSS = '''
*{box-sizing:border-box}body{margin:0;background:#e9eeeb;color:#192b29;font-family:Arial,Helvetica,sans-serif}.board{width:1600px;min-height:1100px;padding:45px 52px 35px}.board-heading{display:flex;justify-content:space-between;gap:30px;align-items:center;margin-bottom:35px}.heading-left{display:flex;align-items:center;gap:22px}.hero-mark{width:84px;height:84px;border-radius:20px;background:#142627;display:flex;align-items:center;justify-content:center;padding:17px}.hero-mark svg{width:100%;height:100%}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#61746b;margin:0 0 10px}.board h1{font-size:34px;font-weight:500;letter-spacing:-.03em;margin:0}.concept-note{font-size:13px;color:#61746b;max-width:390px;line-height:1.5;margin:0}.applications{display:grid;grid-template-columns:1040px 420px;gap:36px;align-items:start}.application-label{font-size:12px;letter-spacing:.08em;margin:0 0 14px;text-transform:uppercase;color:#61746b}.website{width:1040px;height:730px;background:#faf7f2;border-radius:12px;overflow:hidden;border:1px solid #d4dbd6}.browser-bar{height:36px;display:flex;align-items:center;padding:0 16px;background:#f2f4f0;border-bottom:1px solid #d4dbd6}.browser-dots{display:flex;gap:6px}.browser-dots i{width:7px;height:7px;border-radius:50%;background:#bdc8c1}.browser-title{font-size:10px;letter-spacing:.06em;margin:auto;color:#7a8b80}.website-nav{height:94px;background:#142627;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 36px;gap:18px}.site-brand{display:flex;align-items:center;gap:13px;min-width:225px}.site-logo{width:51px;height:55px}.site-logo svg{width:100%;height:100%}.site-brand>span{font-size:24px;letter-spacing:-.04em}.site-brand small{display:block;font-size:11px;letter-spacing:.08em;margin-top:3px}.wordmark-brand{width:170px;height:66px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:5px}.wordmark-brand svg{width:126px;height:40px}.wordmark-brand>span{font-size:10px;letter-spacing:.17em;margin-left:3px}.wordmark-brand.motion{gap:4px}.wordmark-brand.motion svg{width:140px;height:29px}.nav-items{display:flex;align-items:center;gap:24px;font-size:12px;color:#e5efeb}.site-cta{font-size:11px;background:#bcf7f3;color:#142627;padding:13px 17px;border-radius:5px}.site-hero{height:525px;display:grid;grid-template-columns:1.25fr .9fr;gap:35px;padding:38px 36px 30px}.hero-copy{padding-top:25px}.site-kicker{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#597368;margin:0 0 22px}.site-hero h2{font-size:47px;line-height:1.09;font-weight:400;letter-spacing:-.05em;margin:0 0 22px}.site-hero h2 span{display:block}.site-hero h2 em{font-style:normal;color:#6a8c81}.site-lead{font-size:13px;line-height:1.65;color:#627369;max-width:420px}.site-actions{display:flex;gap:13px;margin-top:28px;align-items:center;font-size:12px}.site-actions .primary{background:#142627;color:#fff;padding:15px 20px;border-radius:5px}.site-actions .secondary{padding:13px 9px;color:#3e594f}.hero-photo{height:457px;overflow:hidden;border-radius:90px 12px 12px 12px}.hero-photo img{width:100%;height:100%;object-fit:cover;object-position:center 45%}.site-footer-strip{margin:0 36px;display:flex;gap:20px;padding-top:18px;border-top:1px solid #d8dfd8;font-size:11px;color:#61746b}.site-footer-strip span+span:before{content:'·';margin-right:20px;color:#76958a}.website-notes{margin-top:24px;display:grid;grid-template-columns:1fr 1fr;gap:35px;color:#61746b;font-size:12px;line-height:1.6}.website-notes p{margin:0}.website-notes strong{font-weight:500;color:#243c32;display:block;margin-bottom:6px}.instagram{width:420px;height:812px;border-radius:28px;background:#fff;border:1px solid #d2d9d5;color:#111;overflow:hidden;position:relative}.phone-status{display:flex;justify-content:space-between;font-size:11px;font-weight:bold;height:38px;padding:14px 25px 5px}.instagram-top{height:46px;display:flex;justify-content:space-between;align-items:center;padding:0 21px;font-size:17px;font-weight:bold}.ig-top-icons{font-size:23px;font-weight:400;letter-spacing:10px}.profile-head{display:flex;align-items:center;gap:22px;padding:13px 21px 16px}.avatar-ring{flex-shrink:0;width:88px;height:88px;border-radius:50%;border:2px solid #bcf7f3;padding:4px}.avatar{width:100%;height:100%;border-radius:50%;background:#142627;display:flex;align-items:center;justify-content:center;padding:15px}.avatar svg{width:100%;height:100%}.profile-stats{display:flex;justify-content:space-between;flex:1;gap:15px;text-align:center;font-size:10px}.profile-stats b{display:block;font-size:19px;font-weight:600;margin-bottom:5px}.profile-bio{padding:0 23px;font-size:12px;line-height:1.55}.profile-bio b{display:block;font-weight:600}.profile-bio .category{color:#8b8b8b;font-size:11px}.bio-link{color:#193e61;font-weight:bold;margin-top:4px}.ig-actions{display:flex;gap:7px;margin:14px 21px 16px}.ig-actions span{flex:1;text-align:center;padding:8px;border-radius:6px;font-size:11px;background:#efefef;font-weight:bold}.ig-actions .follow{background:#4197f5;color:#fff}.highlights{display:flex;gap:23px;padding:0 24px 16px}.highlight{text-align:center;font-size:9px}.highlight i{width:49px;height:49px;border:1px solid #d9dfda;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:17px;color:#3d5f53;background:#edf5f1;margin-bottom:5px}.highlight:nth-child(2) i{background:#e5f7f4}.highlight:nth-child(3) i{background:#f2e9ef}.tabs{height:38px;border-top:1px solid #eee;display:flex;justify-content:space-around;align-items:center;color:#8d8d8d}.tabs span{font-size:21px}.tabs span:first-child{color:#111}.post-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}.post-grid>div{height:159px;position:relative;overflow:hidden}.post-grid img{width:100%;height:100%;object-fit:cover;object-position:50% 44%}.post-grid .post-brand{background:#142627;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:13px;color:#fff;text-align:center}.post-brand .post-mark{width:64px;height:65px}.post-mark svg{width:100%;height:100%}.post-brand p{font-size:15px;line-height:1.1;letter-spacing:-.04em;margin:0}.post-brand small{font-size:6px;letter-spacing:.14em;color:#bcf7f3}.post-grid .mint-post{background:#bcf7f3;color:#19372f;display:flex;align-items:center;justify-content:center;text-align:left;font-size:24px;line-height:1.08;letter-spacing:-.04em}.photo-logo{position:absolute;bottom:9px;right:9px;width:29px;height:29px;background:#142627;border-radius:50%;padding:6px}.photo-logo svg{width:100%;height:100%}.ig-bottom{position:absolute;bottom:0;left:0;right:0;height:40px;display:flex;align-items:center;justify-content:space-around;background:white;border-top:1px solid #eee;font-size:22px}.mini-avatar{width:22px;height:22px;background:#142627;border-radius:50%;padding:5px}.mini-avatar svg{width:100%;height:100%}.social-note{font-size:11px;line-height:1.55;color:#61746b;margin:16px 0 0}.board-footer{margin-top:25px;padding-top:17px;border-top:1px solid #d1dad3;display:flex;justify-content:space-between;color:#61746b;font-size:11px;line-height:1.5}
'''

for i, c in enumerate(concepts, 1):
    hero_logo = mark(c, 'hero')
    avatar_logo = mark(c, 'avatar')
    post_logo = mark(c, 'post')
    photo_logo = mark(c, 'photo')
    mini_logo = mark(c, 'mini')
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
    <header class="board-heading"><div class="heading-left"><div class="hero-mark">{hero_logo}</div><div><p class="eyebrow">Tatsi in motion / {i:02d} of 10</p><h1>{escape(c['name'])}</h1></div></div><p class="concept-note">{escape(c['idea'])}</p></header>
    <div class="applications"><section><p class="application-label">01 / Сайт · шапка и первый экран</p>{website}<div class="website-notes"><p><strong>Белый + #bcf7f3</strong>Тёмная шапка даёт контраст светлому логотипу. В макете использованы фотография и тексты существующего сайта.</p><p><strong>Один знак в разных размерах</strong>Геометрия и цвета совпадают с SVG. Здесь скорректированы только размер и свободное поле вокруг знака.</p></div></section><section><p class="application-label">02 / Instagram · аватар и публикации</p>{instagram}<p class="social-note">Макет профиля. Имя пользователя — пример; показатели не указаны. Публикации иллюстрируют оформление.</p></section></div>
    <footer class="board-footer"><span>Вариант {i:02d} · {escape(c['ru'])} · локальная примерка логотипа</span><span>SVG сохранён отдельно · 25.10.2026</span></footer>
    </main></body></html>'''
    (OUT / (c['slug'] + '.html')).write_text(html)

sections = []
for i, c in enumerate(concepts, 1):
    slug = c['slug']
    sections.append(f'''<section id="panel-{i:02d}" role="tabpanel" aria-labelledby="tab-{i:02d}" tabindex="0" {"hidden" if i != 1 else ""}><div class="section-title"><h2>{i:02d} / {escape(c['name'])}</h2><a href="svg/{slug}.svg" download>Скачать SVG ↓</a></div><a href="applications/{slug}-board.png" target="_blank"><img src="applications/{slug}-board.png" alt="{escape(c['name'])}: пример на сайте и в Instagram" loading="eager" width="1600" height="1200"></a><div class="links"><a href="applications/{slug}-website.png" target="_blank">Сайт отдельно ↗</a><a href="applications/{slug}-instagram.png" target="_blank">Instagram отдельно ↗</a><a href="applications/{slug}.html" target="_blank">Макет HTML ↗</a></div></section>''')
apps_gallery = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tatsi in motion — сайт и Instagram</title><style>*{box-sizing:border-box}body{margin:0;background:#0b1516;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1400px;margin:auto;padding:40px 28px}a{color:#bcf7f3;text-decoration:none}h1{font-size:clamp(30px,4vw,50px);font-weight:450;letter-spacing:-.035em;margin:22px 0 15px}.intro{max-width:780px;color:#adc0b8;line-height:1.6}nav{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 36px}nav a{padding:10px 15px;border:1px solid #385249;border-radius:4px}nav a[aria-selected="true"]{background:#bcf7f3;color:#142627;border-color:#bcf7f3}[hidden]{display:none!important}section{margin-bottom:60px;scroll-margin-top:20px}.section-title{display:flex;justify-content:space-between;align-items:center;gap:20px}.section-title h2{font-size:22px;font-weight:500}.section-title a,.links{font-size:13px}section img{display:block;width:100%;height:auto;border-radius:6px}.links{display:flex;flex-wrap:wrap;gap:25px;margin-top:18px}a:focus-visible{outline:2px solid #bcf7f3;outline-offset:4px}.download{display:inline-block;padding:12px 18px;background:#bcf7f3;color:#142627;border-radius:4px}@media(max-width:600px){main{padding:25px 15px}.section-title{align-items:start}.section-title h2{font-size:17px}.section-title a{font-size:11px}section{margin-bottom:35px}nav{gap:6px}nav a{padding:8px 12px}.links{gap:16px}section img{min-width:0}}</style></head><body><main><a href="index.html">← Все логотипы</a><h1>Сайт + Instagram.</h1><p class="intro">Наведите мышку на номер — ниже сразу появится этот вариант на сайте и в Instagram. На телефоне нажмите на номер.</p><a class="download" href="tatsi-in-motion-preview-pack.zip" download>Скачать все SVG и макеты ↓</a><nav role="tablist" aria-label="Выбрать вариант">NAV</nav>SECTIONS</main><script src="applications.js"></script></body></html>'''
apps_gallery = apps_gallery.replace('NAV', ''.join(f'<a href="#concept-{i:02d}" id="tab-{i:02d}" role="tab" aria-controls="panel-{i:02d}" aria-selected="{str(i == 1).lower()}" tabindex="{0 if i == 1 else -1}">{i:02d}</a>' for i in range(1, 11))).replace('SECTIONS', '\n'.join(sections))
(ROOT / 'applications.html').write_text(apps_gallery)

# Extend the task-owned overview without touching the production landing page.
gallery_path = ROOT / 'index.html'
gallery = gallery_path.read_text()
gallery = gallery.replace('<section class="grid"', '<p style="margin:0 0 26px"><a href="applications.html" style="color:#bcf7f3;text-decoration:none;font-size:16px">Посмотреть все 10 вариантов на сайте и в Instagram →</a></p><section class="grid"')
for i, c in enumerate(concepts, 1):
    target = f'<p class="rationale">{c["idea"]}</p>'
    link = f'<p style="margin:14px 0 0;font-size:12px"><a href="applications.html#concept-{i:02d}" style="color:#bcf7f3;text-decoration:none">Сайт + Instagram →</a></p>'
    gallery = gallery.replace(target, target + link)
gallery_path.write_text(gallery)
print('Created 10 context boards and an applications gallery.')
