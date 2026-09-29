/*
    Variant A motion layer. Runs after script.js, which still owns i18n,
    the mobile menu, the form and the .reveal observer.
*/
(function () {
    'use strict';

    const hero = document.querySelector('.hero');
    const heroTitle = document.querySelector('.hero h1');
    const header = document.querySelector('.site-header');

    /* Split the headline into its sentences so each line enters on its own.
       i18n replaces textContent on language change, so we re-split afterwards. */
    function splitHeroTitle() {
        if (!heroTitle) return;
        const text = heroTitle.textContent.trim();
        const lines = text.split(/(?<=\.)\s+/).filter(Boolean);
        heroTitle.innerHTML = lines
            .map((line, i) => `<span class="line" data-enter style="--i:${i + 1}">${line}</span>`)
            .join('');
    }

    /* script.js applies the saved language on DOMContentLoaded and rewrites the
       headline, so the split (and the entrance) must run after that handler. */
    document.addEventListener('DOMContentLoaded', () => {
        splitHeroTitle();
        if (hero) {
            requestAnimationFrame(() => hero.classList.add('is-active'));
            window.setTimeout(() => hero.classList.add('settled'), 1600);
        }
    });
    document.querySelectorAll('[data-lang-switch]').forEach((button) => {
        button.addEventListener('click', () => setTimeout(splitHeroTitle, 0));
    });

    /* Header state after the first screen. */
    function onScroll() {
        if (header) header.classList.toggle('scrolled', window.scrollY > 40);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* FAQ accordion (replaces <details>, which cannot animate). */
    document.querySelectorAll('.faq-item').forEach((item) => {
        const button = item.querySelector('.faq-q');
        if (!button) return;
        button.addEventListener('click', () => {
            const open = item.classList.toggle('open');
            button.setAttribute('aria-expanded', String(open));
        });
    });
})();
