/*
    Variant B motion layer: everything from Variant A plus inertia scrolling
    (Lenis) and the pinned offer beats. Native CSS scroll-driven animations
    handle the parallax and the process line; see style.css.
*/
(function () {
    'use strict';

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const hero = document.querySelector('.hero');
    const heroTitle = document.querySelector('.hero h1');
    const header = document.querySelector('.site-header');

    function splitHeroTitle() {
        if (!heroTitle) return;
        const lines = heroTitle.textContent.trim().split(/(?<=\.)\s+/).filter(Boolean);
        heroTitle.innerHTML = lines
            .map((line, i) => `<span class="line" data-enter style="--i:${i + 1}">${line}</span>`)
            .join('');
    }

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

    /* Inertia scrolling. Skipped for reduced motion; native scroll stays. */
    if (!reduced && typeof window.Lenis === 'function') {
        const lenis = new window.Lenis({ lerp: 0.09, anchors: true });
        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
    }

    function onScroll() {
        if (header) header.classList.toggle('scrolled', window.scrollY > 40);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* Offer beats: the one nearest the viewport centre is active. */
    const beats = Array.from(document.querySelectorAll('#beats .beat'));
    if (beats.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    beats.forEach((beat) => beat.classList.toggle('active', beat === entry.target));
                }
            });
        }, { rootMargin: '-42% 0px -42% 0px', threshold: 0 });
        beats.forEach((beat) => observer.observe(beat));
    }

    document.querySelectorAll('.faq-item').forEach((item) => {
        const button = item.querySelector('.faq-q');
        if (!button) return;
        button.addEventListener('click', () => {
            const open = item.classList.toggle('open');
            button.setAttribute('aria-expanded', String(open));
        });
    });
})();
