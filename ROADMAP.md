# Tatsiana Rukhlenko Landing - Future Plan

This roadmap lists work that should happen after the static MVP is reviewed.

## Before Public Launch

- Replace `Adresse folgt` with the real business address required for the German Impressum.
- Replace `USt-IdNr.: folgt` only after the real VAT ID is confirmed. Do not use the temporary `123456789` value.
- Add verified qualification and certification details.
- Have the final `Impressum` and `Datenschutzerklärung` reviewed by a qualified German legal/privacy source.
- Replace the Calendly placeholder with the real booking link.

## Booking And Forms

- Decide whether Calendly should open as an external link or be embedded directly on the page.
- If Calendly is embedded, update the privacy policy because a third-party widget will load.
- Consider replacing the current `mailto:` fallback with a real form service or backend endpoint.
- If a form service is used, document where form data is stored and how long it is retained.

## Analytics And Consent

- The MVP intentionally has no analytics or tracking.
- Future analytics options:
  - Plausible, Fathom, or Vercel Analytics for privacy-friendly traffic insight.
  - Google Analytics or Meta Pixel only if advertising/tracking is required.
- If analytics, pixels, maps, videos, or embedded widgets are added, implement consent before those tools load.
- Add a cookie/settings control so users can change consent later.

## Content Growth

- Add client testimonials only with explicit permission.
- Add before/after or transformation content only with explicit written consent.
- Add service/package details after Tatsiana confirms the exact offer.
- Add a blog or short articles later for SEO around mobility, posture, flexibility, and beginner-friendly training.

## Deployment

- Choose hosting: static hosting, Vercel, Netlify, or another provider.
- Add domain, SSL, and production metadata.
- Verify mobile, desktop, accessibility, language switching, and legal footer links before launch.
