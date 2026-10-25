"""Brand-kit overview board (3 × 3) for one logo direction, following the brandkit skill's panel system.

The skill as written prompts an image model; this builds the same board from the real vector assets and the
site's own photos and copy, as HTML (rendered to PNG with the logo-design skill's render_png.py).
Usage:  python3 build-brandboard.py 62-curl-wave 67-curl-wave-dark
        (light master for white panels, dark master for dark panels)
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
light = sys.argv[1] if len(sys.argv) > 1 else '62-curl-wave'
dark = sys.argv[2] if len(sys.argv) > 2 else '67-curl-wave-dark'
OUT = ROOT / 'preview' / f'brand-board-{light}.html'

CSS = '''
*{box-sizing:border-box}body{margin:0;background:#1a1d1f;color:#e8e6e1;font-family:"Avenir Next","Segoe UI",Helvetica,Arial,sans-serif}
.board{width:1600px;height:1200px;padding:44px 48px 40px;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:auto repeat(3,1fr);gap:22px}
.head{grid-column:1/-1;display:flex;justify-content:space-between;align-items:baseline;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8b918f;padding-bottom:4px}
.p{position:relative;border-radius:10px;overflow:hidden;background:#242829}.p .lbl{position:absolute;left:16px;bottom:12px;font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:#8b918f}
.p .num{position:absolute;right:16px;top:12px;font-size:9px;letter-spacing:.12em;color:#8b918f}
.light{background:#faf7f2;color:#211d26}.light .lbl,.light .num{color:#8f8a94}
.cover{display:flex;align-items:center;justify-content:center}.cover img{width:62%;height:62%}
.mint{background:#bcf7f3;color:#211d26}.mint .lbl,.mint .num{color:#3f6d68}
.construct{display:flex;align-items:center;justify-content:center}.construct svg{width:72%;height:72%}
.digital{background:#142627;display:flex;align-items:center;justify-content:center;padding:34px}.digital .browser{width:100%;background:#faf7f2;border-radius:8px;overflow:hidden;border:1px solid #2b3a3a}
.bar{height:22px;background:#f2f4f0;display:flex;align-items:center;gap:5px;padding:0 10px}.bar i{width:6px;height:6px;border-radius:50%;background:#c9d1cb}
.nav{height:54px;background:#142627;display:flex;align-items:center;justify-content:space-between;padding:0 18px;color:#fff}.nav .brand{display:flex;align-items:center;gap:10px;font-size:14px}.nav .brand img{width:34px;height:34px}.nav .brand small{display:block;font-size:7px;letter-spacing:.1em}
.nav .cta{font-size:8px;background:#bcf7f3;color:#142627;padding:7px 10px;border-radius:3px}.hero{padding:18px 18px 16px;color:#211d26}.hero h3{font-weight:400;font-size:22px;line-height:1.1;margin:0 0 8px;letter-spacing:-.03em}.hero h3 em{font-style:normal;color:#6a8c81}.hero p{font-size:8px;color:#627369;margin:0;max-width:60%}
.essence{display:flex;align-items:center;justify-content:center;text-align:center;padding:40px}.essence h2{font-weight:400;font-size:40px;line-height:1.1;letter-spacing:-.03em;margin:0}.essence h2 span{display:block;color:#bcf7f3}
.colors{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:0}.colors .lbl{bottom:auto;top:12px}.sw{display:flex;align-items:flex-end;padding:12px;font-size:9px;letter-spacing:.08em}.sw span{display:block}
.type{padding:34px 36px;display:flex;flex-direction:column;justify-content:space-between}.type .big{font-family:Zapfino,"Snell Roundhand",cursive;font-size:84px;line-height:1;color:#86e3da;margin-left:10px}.type .serif{font-family:Didot,"Bodoni 72",serif;font-size:30px;letter-spacing:.02em;color:#211d26}.type .sans{font-size:12px;color:#62586a;line-height:1.5}.type .sans b{display:block;color:#211d26;font-weight:600;letter-spacing:.08em;font-size:10px;text-transform:uppercase;margin-bottom:4px}
.physical{display:flex;align-items:center;justify-content:center;background:#2b2f30}.card{width:300px;height:172px;border-radius:8px;background:#faf7f2;box-shadow:0 20px 40px rgba(0,0,0,.45);position:relative;color:#211d26;transform:rotate(-6deg)}
.card img{position:absolute;left:22px;top:20px;width:64px;height:64px}.card .nm{position:absolute;left:24px;bottom:26px;font-size:12px;letter-spacing:.04em}.card .nm small{display:block;font-size:8px;letter-spacing:.14em;color:#62586a;margin-top:3px}.card .mk{position:absolute;right:0;top:0;bottom:0;width:10px;background:#bcf7f3;border-radius:0 8px 8px 0}
.image{background:#111}.image img{width:100%;height:100%;object-fit:cover;object-position:50% 40%;filter:saturate(.8) contrast(1.05)}.image:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,38,39,.1),rgba(20,38,39,.55))}.image .ov{position:absolute;left:18px;top:16px;width:42px;height:42px;z-index:2}
.system{display:grid;grid-template-columns:repeat(4,1fr);align-items:center;justify-items:center;padding:30px 24px 44px;gap:10px}.system .fav{width:16px;height:16px}.system .fav32{width:32px;height:32px}.system .tile{width:64px;height:64px;border-radius:14px;background:#142627;display:flex;align-items:center;justify-content:center}.system .tile img{width:70%;height:70%}
.system .av{width:64px;height:64px;border-radius:50%;background:#142627;border:2px solid #bcf7f3;display:flex;align-items:center;justify-content:center}.system .av img{width:66%;height:66%}
.system .chip{grid-column:1/-1;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#8b918f;border:1px solid #3a3f41;border-radius:20px;padding:7px 14px;display:flex;gap:10px;align-items:center}.system .chip img{width:14px;height:14px}
'''

light_svg = f'../svg/{light}.svg'
dark_svg = f'../svg/{dark}.svg'
construction = '''<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#9aa3a0" stroke-width="1">
<circle cx="256" cy="256" r="200" stroke-dasharray="4 6"/><circle cx="256" cy="256" r="100" stroke-dasharray="2 8" opacity=".5"/>
<line x1="256" y1="30" x2="256" y2="482" stroke-dasharray="4 6" opacity=".6"/><line x1="30" y1="256" x2="482" y2="256" stroke-dasharray="4 6" opacity=".6"/>
<path d="M84 236 C170 196 300 268 468 220" stroke="#bcf7f3" stroke-width="2"/><path d="M84 236 L170 196 M300 268 L468 220" stroke="#5e6664" stroke-dasharray="3 4"/>
<circle cx="170" cy="196" r="3" fill="#5e6664" stroke="none"/><circle cx="300" cy="268" r="3" fill="#5e6664" stroke="none"/>
<path d="M256 256 L449 204" stroke="#5e6664" stroke-dasharray="3 4"/><text x="300" y="248" font-size="11" fill="#9aa3a0" stroke="none" font-family="Helvetica">r = 200</text>
<path d="M349 85 A200 200 0 0 1 449 204" stroke="#bcf7f3" stroke-width="2" opacity=".5"/><text x="420" y="110" font-size="11" fill="#9aa3a0" stroke="none" font-family="Helvetica">gap 55°</text>
<text x="40" y="470" font-size="11" fill="#9aa3a0" stroke="none" font-family="Helvetica" letter-spacing="2">RING 6 · WAVE 8→0 · ZAPFINO t 270</text>
</svg>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Brand board · Tatsi in motion</title><style>{CSS}</style></head><body><div class="board">
<div class="head"><span>Tatsi in motion · brand kit · direction {light[:2]}</span><span>Mobility &amp; fitness coaching · 25.10.2026</span></div>
<div class="p light cover"><img src="{light_svg}" alt=""><span class="num">01</span><span class="lbl">Logo</span></div>
<div class="p construct">{construction}<span class="num">02</span><span class="lbl">Construction</span></div>
<div class="p digital"><div class="browser"><div class="bar"><i></i><i></i><i></i></div><div class="nav"><div class="brand"><img src="{dark_svg}" alt=""><span>Tatsi <small>IN MOTION</small></span></div><span class="cta">Kostenlose Beratung ↗</span></div><div class="hero"><h3>Freier bewegen.<br>Stärker trainieren.<br><em>Besser fühlen.</em></h3><p>Kostenlose Online-Beratung für Erwachsene, die mehr Bewegungsfreiheit suchen.</p></div></div><span class="num">03</span><span class="lbl">Digital</span></div>
<div class="p essence"><h2>Move freely.<span>Feel strong.</span></h2><span class="num">04</span><span class="lbl">Essence</span></div>
<div class="p colors"><div class="sw" style="background:#faf7f2;color:#211d26"><span>Paper<br>#FAF7F2</span></div><div class="sw" style="background:#211d26;color:#faf7f2"><span>Ink<br>#211D26</span></div><div class="sw" style="background:#bcf7f3;color:#211d26"><span>Mint<br>#BCF7F3</span></div><div class="sw" style="background:#86e3da;color:#211d26"><span>Mint on paper<br>#86E3DA</span></div><div class="sw" style="background:#ede1ef;color:#211d26"><span>Lavender<br>#EDE1EF</span></div><div class="sw" style="background:#b9a3c8;color:#211d26"><span>Accent<br>#B9A3C8</span></div><span class="num">05</span><span class="lbl" style="color:#3f6d68">Color</span></div>
<div class="p light type"><div class="big">t</div><div class="serif">Tatsi in motion</div><div class="sans"><b>Zapfino · Didot · Avenir Next</b>Script letter for the mark, Didone for the name, Avenir Next for everything that has to be read.</div><span class="num">06</span><span class="lbl">Type</span></div>
<div class="p physical"><div class="card"><img src="{light_svg}" alt=""><div class="nm">Tatsiana<small>TATSI IN MOTION · MOBILITY COACH</small></div><div class="mk"></div></div><span class="num">07</span><span class="lbl">Print</span></div>
<div class="p image"><img src="../../../images/tatsiana-mobility.jpg" alt=""><img class="ov" src="{dark_svg}" alt=""><span class="num" style="z-index:2;color:#e8e6e1">08</span><span class="lbl" style="z-index:2;color:#e8e6e1">Image</span></div>
<div class="p system"><img class="fav" src="{dark_svg}" alt=""><img class="fav32" src="{dark_svg}" alt=""><div class="tile"><img src="{dark_svg}" alt=""></div><div class="av"><img src="{dark_svg}" alt=""></div><div class="chip"><img src="{dark_svg}" alt="">tatsi.in.motion · follow</div><span class="num">09</span><span class="lbl">System</span></div>
</div></body></html>'''
OUT.write_text(html)
print(OUT)
