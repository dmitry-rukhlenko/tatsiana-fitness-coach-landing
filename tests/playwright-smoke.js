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

    /*
     * The legal notice is intentionally a separate page.
     * This catches broken footer links when files are renamed or moved.
     */
    const impressumHref = await page.locator('footer a[href="impressum.html"]').getAttribute('href');
    if (impressumHref !== 'impressum.html') {
        throw new Error(`Expected footer Impressum link to point to impressum.html, found "${impressumHref}".`);
    }

    await page.goto(pathToFileURL(path.join(projectRoot, 'impressum.html')).href);

    const impressumTitle = await page.locator('h1').textContent();
    if (impressumTitle.trim() !== 'Imprint') {
        throw new Error(`Unexpected Impressum page title: "${impressumTitle}".`);
    }

    const ddgText = await page.locator('main').textContent();
    if (!ddgText.includes('Section 5 DDG')) {
        throw new Error('Impressum page does not mention § 5 DDG.');
    }

    await page.getByRole('button', { name: 'DE', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'de');

    const germanImpressumTitle = await page.locator('h1').textContent();
    if (germanImpressumTitle.trim() !== 'Impressum') {
        throw new Error(`Language switch did not update the Impressum title: "${germanImpressumTitle}".`);
    }

    await browser.close();
    console.log('Playwright smoke test passed.');
}

runSmokeTest().catch((error) => {
    console.error(error);
    process.exit(1);
});
