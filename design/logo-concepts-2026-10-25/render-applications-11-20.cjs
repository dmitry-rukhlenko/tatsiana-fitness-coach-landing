// Render boards 11-20 to PNG (board, website, instagram) with the same checks as render-applications.cjs.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

async function main() {
  const root = __dirname;
  const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts-11-20.json')));
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
    for (const concept of concepts) {
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
        // Stroke-aware clipping check: the geometry plus half the stroke must stay inside the cropped viewBox.
        const clipped = svgs.flatMap(svg => {
          const v = svg.viewBox.baseVal;
          const shapes = Array.from(svg.querySelectorAll('path, circle, rect, polygon, line, ellipse'));
          const bad = shapes.some(shape => {
            // getBBox is in the shape's own coordinates; map it into the svg's user space (handles <g transform>).
            const m = svg.getScreenCTM().inverse().multiply(shape.getScreenCTM());
            const bb = shape.getBBox();
            const corners = [[bb.x, bb.y], [bb.x + bb.width, bb.y], [bb.x, bb.y + bb.height], [bb.x + bb.width, bb.y + bb.height]]
              .map(([x, y]) => ({ x: m.a * x + m.c * y + m.e, y: m.b * x + m.d * y + m.f }));
            const b = {
              x: Math.min(...corners.map(p => p.x)), y: Math.min(...corners.map(p => p.y)),
              x2: Math.max(...corners.map(p => p.x)), y2: Math.max(...corners.map(p => p.y)),
            };
            const sw = shape.getAttribute('stroke') === 'none' ? 0 : parseFloat(getComputedStyle(shape).strokeWidth) || 0;
            const h = sw / 2;
            return b.x - h < v.x || b.y - h < v.y || b.x2 + h > v.x + v.width || b.y2 + h > v.y + v.height;
          });
          return bad ? [svg.getAttribute('aria-labelledby')] : [];
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
      console.log(`Rendered ${reports.length}/${concepts.length}: ${concept.slug}`);
    }
    fs.writeFileSync(path.join(root, 'applications-verification-11-20.json'), JSON.stringify(reports, null, 2) + '\n');
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error.message); process.exit(1); });
