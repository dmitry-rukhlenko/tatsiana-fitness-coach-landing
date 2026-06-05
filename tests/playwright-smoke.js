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
        situationItems: document.querySelectorAll('.situation-item').length,
        serviceTopics: document.querySelectorAll('.service-topic').length,
        servicesImages: document.querySelectorAll('#services .services-feature-media img').length,
        contactRows: document.querySelectorAll('.contact-row').length,
        legalSections: document.querySelectorAll('.legal-section').length,
        trackingScripts: [...document.scripts].filter((script) => {
            const content = `${script.src} ${script.textContent}`;
            return /gtag|analytics|pixel|facebook|google-analytics/i.test(content);
        }).length
    }));

    if (counts.infoTiles !== 4) {
        throw new Error(`Expected 4 info tiles, found ${counts.infoTiles}.`);
    }

    if (counts.situationItems !== 3) {
        throw new Error(`Expected 3 situation items, found ${counts.situationItems}.`);
    }

    if (counts.serviceTopics !== 6) {
        throw new Error(`Expected 6 service topics, found ${counts.serviceTopics}.`);
    }

    if (counts.servicesImages !== 1) {
        throw new Error(`Expected 1 image-led services visual, found ${counts.servicesImages}.`);
    }

    if (counts.contactRows !== 2) {
        throw new Error(`Expected 2 contact rows, found ${counts.contactRows}.`);
    }

    if (counts.legalSections !== 0) {
        throw new Error(`Expected legal details to live on the legal page, found ${counts.legalSections} homepage legal sections.`);
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

    const privacyHref = await page.locator('footer a[href="impressum.html#privacy"]').getAttribute('href');
    if (privacyHref !== 'impressum.html#privacy') {
        throw new Error(`Expected footer privacy link to point to impressum.html#privacy, found "${privacyHref}".`);
    }

    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(siteUrl);

    const mobileConversionBar = page.locator('.mobile-conversion-bar');
    const mobileBarState = await mobileConversionBar.evaluate((element) => {
        const style = window.getComputedStyle(element);
        const primary = element.querySelector('.mobile-conversion-primary');
        const secondary = element.querySelector('.mobile-conversion-secondary');

        return {
            display: style.display,
            pointerEvents: style.pointerEvents,
            primaryHeight: primary.getBoundingClientRect().height,
            secondaryHeight: secondary.getBoundingClientRect().height,
            primaryHref: primary.getAttribute('href'),
            secondaryHref: secondary.getAttribute('href')
        };
    });

    if (mobileBarState.display === 'none') {
        throw new Error('Expected the mobile conversion bar to be visible on a phone viewport.');
    }

    if (mobileBarState.primaryHref !== '#consultation') {
        throw new Error(`Expected mobile primary CTA to point to #consultation, found "${mobileBarState.primaryHref}".`);
    }

    if (!mobileBarState.secondaryHref.startsWith('mailto:tatsiana.rukhlenko@gmail.com')) {
        throw new Error(`Expected mobile secondary CTA to be an email link, found "${mobileBarState.secondaryHref}".`);
    }

    if (mobileBarState.primaryHeight < 44 || mobileBarState.secondaryHeight < 44) {
        throw new Error(`Expected mobile CTA tap targets to be at least 44px tall, found ${mobileBarState.primaryHeight}px and ${mobileBarState.secondaryHeight}px.`);
    }

    await page.locator('#consultation').scrollIntoViewIfNeeded();
    await page.waitForFunction(() => {
        const bar = document.querySelector('.mobile-conversion-bar');
        const style = window.getComputedStyle(bar);

        return document.body.classList.contains('consultation-in-view')
            && style.opacity === '0'
            && style.pointerEvents === 'none';
    });

    const mobileBarHiddenNearForm = await mobileConversionBar.evaluate((element) => {
        const style = window.getComputedStyle(element);
        return style.opacity === '0' && style.pointerEvents === 'none';
    });

    if (!mobileBarHiddenNearForm) {
        throw new Error('Expected the mobile conversion bar to hide when the consultation form is in view.');
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

    if (await page.locator('#privacy').count() !== 1) {
        throw new Error('Impressum page does not expose a privacy section.');
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
