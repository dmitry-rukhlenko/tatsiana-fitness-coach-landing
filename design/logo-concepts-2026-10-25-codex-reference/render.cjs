// Render task-owned artwork in a fresh, offline browser context, without file navigation.
const {chromium} = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const root = __dirname;
const concepts = JSON.parse(fs.readFileSync(path.join(root, 'concepts-31-40.json')));

function inlineImages(html, folder) {
  return html.replace(/src="([^"#]+)"/g, (original, relative) => {
    if (/^[a-z]+:/i.test(relative)) throw new Error('External source is not allowed');
    const filename = path.resolve(folder, relative);
    const extension = path.extname(filename);
    const mime = extension === '.svg' ? 'image/svg+xml' : extension === '.png' ? 'image/png' : 'image/jpeg';
    return `src="data:${mime};base64,${fs.readFileSync(filename).toString('base64')}"`;
  });
}

async function main() {
  const browser = await chromium.launch({headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  try {
    const page = await browser.newPage({viewport: {width:1800,height:1200}, deviceScaleFactor:1});
    await page.route('**/*', route => route.abort());
    const errors=[];
    page.on('pageerror', error => errors.push(error.message));
    const files=[];
    for (const concept of concepts) {
      const filename = concept.slug + '.svg';
      const svg = fs.readFileSync(path.join(root, 'svg', filename), 'utf8');
      await page.setContent(svg.replace(/<\?xml[^>]*>/, ''));
      const bounds = await page.locator('svg').evaluate(svg => {
        const b = svg.querySelector('g').getBBox();
        return {x:b.x,y:b.y,width:b.width,height:b.height};
      });
      if (bounds.x<16||bounds.y<16||bounds.x+bounds.width>496||bounds.y+bounds.height>496) throw new Error('Out-of-bounds mark: '+filename);
      files.push({file:filename,sha256:crypto.createHash('sha256').update(svg).digest('hex'),bounds});
    }
    await page.setContent(inlineImages(fs.readFileSync(path.join(root,'preview/reference-31-40.html'),'utf8'),path.join(root,'preview')));
    await page.locator('img').evaluateAll(images=>Promise.all(images.map(image=>image.decode())));
    await page.locator('main').screenshot({path:path.join(root,'preview/reference-31-40.png')});
    fs.writeFileSync(path.join(root,'verification-31-40.json'),JSON.stringify({files,errors},null,2)+'\n');

    if (process.argv.includes('--boards')) {
      await page.setViewportSize({width:1600,height:1200});
      const reports=[];
      for (const c of concepts) {
        const filename=path.join(root,'applications',c.slug+'.html');
        await page.setContent(inlineImages(fs.readFileSync(filename,'utf8'),path.dirname(filename)));
        await page.locator('img').evaluateAll(images=>Promise.all(images.map(image=>image.decode())));
        const state=await page.evaluate(()=>{
          const ids=Array.from(document.querySelectorAll('[id]')).map(e=>e.id);
          return {images_loaded:Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0),unique_ids:ids.length===new Set(ids).size,board_in_capture:document.querySelector('.board').getBoundingClientRect().bottom<=innerHeight,overflow:document.documentElement.scrollWidth>innerWidth};
        });
        if(!state.images_loaded||!state.unique_ids||!state.board_in_capture||state.overflow)throw new Error(JSON.stringify({slug:c.slug,...state}));
        await page.screenshot({path:path.join(root,'applications',c.slug+'-board.png')});
        await page.locator('#website-preview').screenshot({path:path.join(root,'applications',c.slug+'-website.png')});
        await page.locator('#instagram-preview').screenshot({path:path.join(root,'applications',c.slug+'-instagram.png')});
        reports.push({slug:c.slug,...state});
        console.log('Rendered '+c.slug);
      }
      fs.writeFileSync(path.join(root,'applications-verification-31-40.json'),JSON.stringify({reports,errors},null,2)+'\n');
    }
    if(errors.length)throw new Error(errors.join('\n'));
    console.log('10 new vector bounds checked; overview rendered. No network requests used.');
  } finally { await browser.close(); }
}

main().catch(error=>{console.error(error.message);process.exit(1)});
