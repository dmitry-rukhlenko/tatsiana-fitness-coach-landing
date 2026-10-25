const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

async function main() {
  const root = __dirname;
  const local = relative => pathToFileURL(path.join(root, relative)).href;
  const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts.json')));
  const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(local('applications.html'));
    await page.locator('img').evaluateAll(images => Promise.all(images.map(image => { image.loading = 'eager'; return image.decode(); })));
    const loaded = await page.locator('img').evaluateAll(images => images.every(image => image.complete && image.naturalWidth === 1600));
    const overflowDesktop = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    await page.screenshot({ path: path.join(root, 'preview/applications-gallery-desktop.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const overflowMobile = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    await page.screenshot({ path: path.join(root, 'preview/applications-gallery-mobile.png') });

    await page.setViewportSize({ width: 1440, height: 1120 });
    const cards = concepts.map((c, index) => `<article><h2>${String(index + 1).padStart(2, '0')} / ${c.name}</h2><div class="samples"><div class="web"><img src="applications/${c.slug}-website.png"></div><div class="ig"><img src="applications/${c.slug}-instagram.png"></div></div></article>`).join('');
    await page.setContent(`<style>*{box-sizing:border-box}body{margin:0;background:#e9eeeb;font:12px Arial;color:#142627}.grid{padding:25px;display:grid;grid-template-columns:1fr 1fr;gap:15px}article{background:white;border-radius:5px;padding:12px;height:200px}h2{font-size:14px;margin:0 0 10px}.samples{display:flex;gap:16px}.web{width:360px;height:100px;overflow:hidden;border-radius:4px;margin-top:20px}.web img{display:block;width:1040px;transform:translate(-5px,-35px)}.ig{width:165px;height:150px;overflow:hidden}.ig img{display:block;width:420px;transform:translate(-8px,-45px)}</style><div class="grid">${cards}</div>`);
    await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
    await page.screenshot({ path: path.join(root, 'preview/placement-review.png') });
    const report = { all_ten_boards_loaded: loaded, desktop_width: 1440, mobile_width: 390, overflowDesktop, overflowMobile, errors };
    fs.writeFileSync(path.join(root, 'gallery-verification.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report));
    if (!loaded || overflowDesktop || overflowMobile || errors.length) throw new Error('Gallery check failed');
  } finally {
    await browser.close();
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
