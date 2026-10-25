// Render task-owned content in an isolated, offline browser. No user tab is opened.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const root = __dirname;
const concepts = JSON.parse(fs.readFileSync(path.join(root,'concepts.json')));
function inlineImages(html, folder) {
  return html.replace(/src="([^"#]+)"/g, (_, relative) => {
    assert(!/^[a-z]+:/i.test(relative),'Unexpected external source');
    const file = path.resolve(folder, relative);
    const mime = file.endsWith('.svg') ? 'image/svg+xml' : file.endsWith('.png') ? 'image/png' : 'image/jpeg';
    return `src="data:${mime};base64,${fs.readFileSync(file).toString('base64')}"`;
  });
}
async function main() {
  const browser = await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  try {
    const page = await browser.newPage({viewport:{width:512,height:512},deviceScaleFactor:2});
    await page.route('**/*',route=>route.abort());
    const errors=[], files=[];
    page.on('pageerror',e=>errors.push(e.message));
    for(const c of concepts) {
      const svg=fs.readFileSync(path.join(root,'svg',c.slug+'.svg'),'utf8');
      await page.setContent('<style>body{margin:0}svg{display:block}</style>'+svg.replace(/<\?xml[^>]*>/,''));
      const bounds=await page.locator('#artwork').evaluate(g=>{
        const b=g.getBBox(); return {x:b.x,y:b.y,width:b.width,height:b.height};
      });
      assert(bounds.x>=16&&bounds.y>=16&&bounds.x+bounds.width<=496&&bounds.y+bounds.height<=496,c.code+' bounds');
      await page.screenshot({path:path.join(root,'png',c.slug+'.png'),omitBackground:true});
      const light=fs.readFileSync(path.join(root,'svg-light',c.slug+'.svg'),'utf8');
      await page.setContent('<style>body{margin:0}svg{display:block}</style>'+light.replace(/<\?xml[^>]*>/,''));
      await page.screenshot({path:path.join(root,'png-light',c.slug+'.png'),omitBackground:true});
      files.push({code:c.code,file:c.slug+'.svg',sha256:crypto.createHash('sha256').update(svg).digest('hex'),bounds});
    }
    fs.writeFileSync(path.join(root,'vector-verification.json'),JSON.stringify({files,errors},null,2)+'\n');
    await page.close();
    const preview=await browser.newPage({viewport:{width:1800,height:1500},deviceScaleFactor:1});
    await preview.route('**/*',route=>route.abort());
    preview.on('pageerror',e=>errors.push(e.message));
    for(const name of ['overview','group-a','group-b','group-c']) {
      const file=path.join(root,'preview',name+'.html');
      await preview.setContent(inlineImages(fs.readFileSync(file,'utf8'),path.dirname(file)));
      await preview.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
      await preview.locator('main').screenshot({path:path.join(root,'preview',name+'.png')});
    }
    console.log('21 SVG bounds checked; 42 transparent 1024px PNGs and 4 overview images rendered.');
    if(process.argv.includes('--boards')) {
      await preview.setViewportSize({width:1600,height:1200});
      const reports=[];
      for(const c of concepts) {
        const file=path.join(root,'applications',c.slug+'.html');
        await preview.setContent(inlineImages(fs.readFileSync(file,'utf8'),path.dirname(file)));
        await preview.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
        const state=await preview.evaluate(()=>{
          const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
          return {images_loaded:[...document.images].every(i=>i.complete&&i.naturalWidth>0),
            unique_ids:ids.length===new Set(ids).size,svgs:document.querySelectorAll('svg').length,
            board_in_capture:document.querySelector('.board').getBoundingClientRect().bottom<=innerHeight,
            overflow:document.documentElement.scrollWidth>innerWidth};
        });
        assert(state.images_loaded&&state.unique_ids&&state.svgs===6&&state.board_in_capture&&!state.overflow,c.code+JSON.stringify(state));
        await preview.screenshot({path:path.join(root,'applications',c.slug+'-board.png')});
        await preview.locator('#website-preview').screenshot({path:path.join(root,'applications',c.slug+'-website.png')});
        await preview.locator('#instagram-preview').screenshot({path:path.join(root,'applications',c.slug+'-instagram.png')});
        reports.push({code:c.code,...state});
        console.log(`Applications ${reports.length}/21: ${c.code}`);
      }
      fs.writeFileSync(path.join(root,'applications-verification.json'),JSON.stringify({reports,errors},null,2)+'\n');
    }
    assert.deepEqual(errors,[]);
  } finally {await browser.close();}
}
main().catch(error=>{console.error(error);process.exit(1)});
