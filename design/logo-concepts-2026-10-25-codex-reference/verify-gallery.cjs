// Serve only this newly generated, task-owned gallery from memory. No file URLs or network.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const root = __dirname;
const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts-31-40.json')));
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
      if (route.request().url() === 'https://tatsi-reference-preview.invalid/') {
        fulfilled++;
        return route.fulfill({ contentType:'text/html', body:html });
      }
      return route.abort();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('https://tatsi-reference-preview.invalid/#concept-34');
    await page.locator('img').evaluateAll(images => Promise.all(images.map(i => i.decode())));
    async function selected(number) {
      assert.equal(await page.locator('[role="tabpanel"]:visible').count(), 1);
      assert.equal(await page.locator('[role="tabpanel"]:visible').getAttribute('id'), 'panel-' + number);
      assert.equal(await page.locator('[aria-selected="true"]').getAttribute('id'), 'tab-' + number);
    }
    await selected('34');
    for (const c of concepts) {
      const n = c.slug.slice(0,2);
      await page.locator('#tab-'+n).hover();
      await selected(n);
      assert.equal(await page.evaluate(() => scrollY), 0);
    }
    await page.locator('#tab-40').focus();
    await page.keyboard.press('Home'); await selected('31');
    await page.keyboard.press('ArrowRight'); await selected('32');
    await page.keyboard.press('End'); await selected('40');
    await page.keyboard.press('ArrowRight'); await selected('31');
    await page.locator('#tab-31').hover();
    await page.screenshot({ path:path.join(root,'preview/gallery-desktop.png'), fullPage:true });
    await page.setViewportSize({ width:390, height:844 });
    await page.locator('#tab-38').click(); await selected('38');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({ path:path.join(root,'preview/gallery-mobile.png'), fullPage:true });

    await page.setViewportSize({ width:1500, height:800 });
    const cards = concepts.map(c => {
      const svg = dataImage(path.join(root,'svg',c.slug+'.svg'));
      return `<article><p>${c.slug.slice(0,2)} / ${c.name}</p><div class="sizes">${[88,52,24].map(s => `<div><img src="${svg}" style="width:${s}px;height:${s}px"><small>${s} px</small></div>`).join('')}</div></article>`;
    }).join('');
    await page.setContent(`<style>*{box-sizing:border-box}body{margin:0;background:#edf0eb;color:#142627;font:14px Arial}main{padding:30px;display:grid;grid-template-columns:repeat(5,1fr);gap:18px}article{padding:18px;background:white}p{margin:0 0 24px}.sizes{display:flex;gap:12px;align-items:center;height:140px}.sizes div{display:flex;flex-direction:column;align-items:center;gap:10px}img{display:block;background:#142627;border-radius:50%}small{color:#566965}</style><main>${cards}</main>`);
    await page.locator('img').evaluateAll(images => Promise.all(images.map(i => i.decode())));
    await page.locator('main').screenshot({ path:path.join(root,'preview/small-sizes.png') });
    assert.deepEqual(errors, []);
    fs.writeFileSync(path.join(root,'gallery-verification.json'), JSON.stringify({
      deep_link:'34', hover_switches:10, only_one_panel:true, no_scroll_jump:true,
      keyboard:'Home, End, ArrowRight and wraparound passed', mobile_click:'38',
      mobile_overflow:false, page_errors:errors, network_requests:0, local_documents_fulfilled:fulfilled
    },null,2)+'\n');
    console.log('PASS: 10 hover switches, deep link, keyboard, mobile click, no overflow, no network.');
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e); process.exit(1); });
