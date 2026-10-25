// Serve only this newly generated, task-owned gallery from memory. No file URLs or network.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const root = __dirname;
const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts.json')));
function dataImage(filename) {
  return `data:image/${filename.endsWith('.svg') ? 'svg+xml' : 'png'};base64,${fs.readFileSync(filename).toString('base64')}`;
}
async function main() {
  const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  try {
    let html = fs.readFileSync(path.join(root, 'applications.html'), 'utf8');
    html = html.replace('<script src="applications.js"></script>', `<script>${fs.readFileSync(path.join(root,'applications.js'),'utf8')}</script>`);
    html = html.replace(/src="([^"]+)"/g, (_, file) => `src="${dataImage(path.join(root,file))}"`);
    const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
    let fulfilled = 0;
    await context.route('**/*', route => {
      if (route.request().url() === 'https://tatsi-refinements-preview.invalid/') {
        fulfilled++;
        return route.fulfill({ contentType:'text/html', body:html });
      }
      return route.abort();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('https://tatsi-refinements-preview.invalid/#concept-B4');
    await page.locator('img').evaluateAll(images => Promise.all(images.map(i => i.decode())));
    async function selected(number) {
      assert.equal(await page.locator('[role="tabpanel"]:visible').count(), 1);
      assert.equal(await page.locator('[role="tabpanel"]:visible').getAttribute('id'), 'panel-' + number);
      assert.equal(await page.locator('[aria-selected="true"]').getAttribute('id'), 'tab-' + number);
      await page.evaluate(() => Promise.all(document.getAnimations().map(animation => animation.finished.catch(() => {}))));
    }
    await selected('B4');
    for (const c of concepts) {
      const n = c.code;
      await page.locator('#tab-'+n).hover();
      await selected(n);
      assert.equal(await page.evaluate(() => scrollY), 0);
    }
    await page.locator('#tab-C7').focus();
    await page.keyboard.press('Home'); await selected('A1');
    await page.keyboard.press('ArrowRight'); await selected('A2');
    await page.keyboard.press('End'); await selected('C7');
    await page.keyboard.press('ArrowRight'); await selected('A1');
    await page.locator('#tab-A1').hover();
    await page.screenshot({ path:path.join(root,'preview/gallery-desktop.png'), fullPage:true });
    await page.setViewportSize({ width:390, height:844 });
    await page.locator('#tab-C5').click(); await selected('C5');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({ path:path.join(root,'preview/gallery-mobile.png'), fullPage:true });

    await page.setViewportSize({ width:1500, height:1600 });
    const cards = concepts.map(c => {
      const svg = dataImage(path.join(root,'svg',c.slug+'.svg'));
      return `<article><p>${c.code} / ${c.name}</p><div class="sizes">${[72,40,24].map(s => `<div><img src="${svg}" style="width:${s}px;height:${s}px"><small>${s} px</small></div>`).join('')}</div></article>`;
    }).join('');
    await page.setContent(`<style>*{box-sizing:border-box}body{margin:0;background:#edf0eb;color:#142627;font:14px Arial}main{padding:30px;display:grid;grid-template-columns:repeat(7,1fr);gap:18px}article{padding:12px;background:white}p{margin:0 0 24px}.sizes{display:flex;gap:8px;align-items:center;height:140px}.sizes div{display:flex;flex-direction:column;align-items:center;gap:10px}img{display:block;background:#142627;border-radius:50%}small{color:#566965}</style><main>${cards}</main>`);
    await page.locator('img').evaluateAll(images => Promise.all(images.map(i => i.decode())));
    await page.locator('main').screenshot({ path:path.join(root,'preview/small-sizes.png') });
    assert.deepEqual(errors, []);
    fs.writeFileSync(path.join(root,'gallery-verification.json'), JSON.stringify({
      deep_link:'B4', hover_switches:21, only_one_panel:true, no_scroll_jump:true,
      keyboard:'Home, End, ArrowRight and wraparound passed', mobile_click:'C5',
      mobile_overflow:false, page_errors:errors, network_requests:0, local_documents_fulfilled:fulfilled
    },null,2)+'\n');
    console.log('PASS: 21 hover switches, deep link, keyboard, mobile click, no overflow, no network.');
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e); process.exit(1); });
