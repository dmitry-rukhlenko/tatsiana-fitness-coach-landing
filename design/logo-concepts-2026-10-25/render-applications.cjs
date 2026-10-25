const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

async function main() {
  const root = __dirname;
  const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts.json')));
  const limit = Number(process.argv[2] || concepts.length);
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  const reports = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 1 });
    let errors = [];
    let remoteRequests = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('request', request => { if (/^https?:/.test(request.url())) remoteRequests.push(request.url()); });
    for (const concept of concepts.slice(0, limit)) {
      errors = [];
      remoteRequests = [];
      await page.goto(pathToFileURL(path.join(root, 'applications', concept.slug + '.html')).href);
      await page.locator('img').evaluateAll(images => Promise.all(images.map(image => image.decode())));
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: path.join(root, 'applications', concept.slug + '-board.png'), fullPage: false });
      await page.locator('#website-preview').screenshot({ path: path.join(root, 'applications', concept.slug + '-website.png') });
      await page.locator('#instagram-preview').screenshot({ path: path.join(root, 'applications', concept.slug + '-instagram.png') });
      const state = await page.evaluate(() => {
        const ids = Array.from(document.querySelectorAll('[id]')).map(el => el.id);
        const board = document.querySelector('.board').getBoundingClientRect();
        const svgs = Array.from(document.querySelectorAll('svg'));
        const clipped = svgs.flatMap(svg => {
          const g = svg.querySelector('g');
          const b = g.getBBox();
          const v = svg.viewBox.baseVal;
          return b.x < v.x || b.y < v.y || b.x + b.width > v.x + v.width || b.y + b.height > v.y + v.height ? [svg.getAttribute('aria-labelledby')] : [];
        });
        return {
          all_images_loaded: Array.from(document.images).every(img => img.complete && img.naturalWidth > 0),
          unique_ids: ids.length === new Set(ids).size,
          svg_count: svgs.length,
          clipped_logos: clipped,
          board_within_capture: board.bottom <= innerHeight,
          horizontal_overflow: document.documentElement.scrollWidth > innerWidth,
        };
      });
      reports.push({ concept: concept.slug, ...state, errors: [...errors], remote_requests: [...remoteRequests] });
      if (!state.all_images_loaded || !state.unique_ids || state.clipped_logos.length || !state.board_within_capture || state.horizontal_overflow || errors.length || remoteRequests.length) {
        throw new Error('Mockup validation failed: ' + JSON.stringify(reports.at(-1)));
      }
      console.log(`Rendered ${reports.length}/${limit}: ${concept.slug}`);
    }
    fs.writeFileSync(path.join(root, 'applications-verification.json'), JSON.stringify(reports, null, 2) + '\n');
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error.message); process.exit(1); });
