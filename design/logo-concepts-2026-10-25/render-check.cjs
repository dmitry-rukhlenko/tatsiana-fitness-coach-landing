const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

async function run() {
  const root = __dirname;
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1200 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    const local = relative => pathToFileURL(path.join(root, relative)).href;
    await page.goto(local('index.html'));
    await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
    const loaded = await page.locator('img').evaluateAll(images => images.every(image => image.complete && image.naturalWidth === 512));
    const desktopOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    await page.screenshot({ path: path.join(root, 'preview/gallery-desktop.png'), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.screenshot({ path: path.join(root, 'preview/gallery-mobile.png') });
    await page.locator('#concept-10').scrollIntoViewIfNeeded();
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await page.screenshot({ path: path.join(root, 'preview/gallery-mobile-last.png') });

    const files = fs.readdirSync(path.join(root, 'svg')).filter(file => file.endsWith('.svg')).sort();
    const bounds = [];
    for (const file of files) {
      await page.goto(local(`svg/${file}`));
      const box = await page.locator('svg').evaluate(svg => {
        const b = svg.querySelector('g').getBBox();
        return { x: b.x, y: b.y, width: b.width, height: b.height };
      });
      if (box.x < 20 || box.y < 20 || box.x + box.width > 492 || box.y + box.height > 492) {
        throw new Error(`Unexpected geometry bounds: ${file}`);
      }
      bounds.push({ file, ...box });
    }

    // Keep the existing file origin so image decoding needs no local HTTP server.
    await page.goto(local('index.html'));
    const small = files.map((file, index) => `<div class="item"><div class="row"><img src="svg/${file}" style="width:48px;height:48px"><img src="svg/${file}" style="width:160px;height:160px"></div><div>${String(index + 1).padStart(2, '0')} — 48 px / 160 px</div></div>`).join('');
    await page.setViewportSize({ width: 1400, height: 660 });
    await page.setContent(`<style>body{margin:0;background:#142627;color:#a3b7b3;font:12px Arial}.grid{padding:30px;display:grid;grid-template-columns:repeat(5,1fr);gap:20px}.row{height:240px;display:flex;align-items:center;justify-content:space-around}.item{border-bottom:1px solid #415b57;padding-bottom:15px}</style><div class="grid">${small}</div>`);
    await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
    await page.screenshot({ path: path.join(root, 'preview/scale-check.png'), fullPage: true });

    const report = JSON.parse(fs.readFileSync(path.join(root, 'verification.json')));
    report.browser = {
      all_images_loaded: loaded,
      desktop_width: 1440, desktop_overflow: desktopOverflow,
      mobile_width: 390, mobile_overflow: mobileOverflow,
      errors, geometry_bounds: bounds,
    };
    fs.writeFileSync(path.join(root, 'verification.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ images: loaded, desktopOverflow, mobileOverflow, errors, geometry_checked: bounds.length }));
    if (!loaded || desktopOverflow || mobileOverflow || errors.length) throw new Error('Preview validation failed');
  } finally {
    await browser.close();
  }
}

run().catch(error => { console.error(error.message); process.exit(1); });
