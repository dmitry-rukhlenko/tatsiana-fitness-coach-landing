const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const projectRoot = path.resolve(__dirname, '..');
const siteUrl = pathToFileURL(path.join(projectRoot, 'index.html')).href;

async function runSmokeTest() {
    /*
     * This is a small visual smoke test, not a full test suite.
     * It opens the static page, checks that key sections exist, and verifies
     * that the language switch changes visible copy from German to English.
     */
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

    await page.goto(siteUrl);

    const title = await page.title();
    if (!title.includes('Tatsiana Rukhlenko')) {
        throw new Error(`Unexpected page title: "${title}"`);
    }

    const counts = await page.evaluate(() => ({
        infoTiles: document.querySelectorAll('.info-tile').length,
        serviceCards: document.querySelectorAll('.service-card').length,
        contactRows: document.querySelectorAll('.contact-row').length,
        trackingScripts: [...document.scripts].filter((script) => {
            const content = `${script.src} ${script.textContent}`;
            return /gtag|analytics|pixel|facebook|google-analytics/i.test(content);
        }).length
    }));

    if (counts.infoTiles !== 4) {
        throw new Error(`Expected 4 info tiles, found ${counts.infoTiles}.`);
    }

    if (counts.serviceCards !== 6) {
        throw new Error(`Expected 6 service cards, found ${counts.serviceCards}.`);
    }

    if (counts.contactRows !== 2) {
        throw new Error(`Expected 2 contact rows, found ${counts.contactRows}.`);
    }

    if (counts.trackingScripts !== 0) {
        throw new Error(`Expected no tracking scripts, found ${counts.trackingScripts}.`);
    }

    await page.getByRole('button', { name: 'EN', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'en');

    const englishHero = await page.locator('h1').textContent();
    if (!englishHero.includes('Move freer')) {
        throw new Error(`Language switch did not update the hero title: "${englishHero}".`);
    }

    await browser.close();
    console.log('Playwright smoke test passed.');
}

runSmokeTest().catch((error) => {
    console.error(error);
    process.exit(1);
});
