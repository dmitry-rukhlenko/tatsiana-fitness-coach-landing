# Tatsiana Rukhlenko Fitness Coach Landing - Requirements Draft

This document is a pre-development specification. It captures the current product goal, reference research, proposed site structure, legal/compliance notes for Germany/EU, asset plan, skill candidates, and open questions that must be answered before implementation.

## 1. Project Goal

Build a modern, responsive landing page for personal fitness coach Tatsiana Rukhlenko.

Primary conversion goal:

- Visitors should book/request a free online consultation.

Current known inputs:

- Coach name: Tatsiana Rukhlenko.
- Market: Germany / European Union.
- Visual direction: modern, pastel, premium, calm, health-focused.
- Device support: desktop and mobile.
- Photo source: Google Drive folder supplied by the client.
- Contact details are pending: Instagram, WhatsApp, email, phone, business address, legal owner data.

Important implementation constraint:

- Do not implement the full site until the section list, content scope, contact flow, legal data, and skill installation choices are approved.

## 2. Current Local Project State

Current files:

- `gemini/index.html`
- `gemini/style.css`
- `gemini/script.js`

The existing local prototype already contains:

- German HTML language setting.
- Hero, about, services, contact, footer.
- Contact form.
- Placeholder legal modals for Impressum and Datenschutz.
- Placeholder contact data.
- Unsplash placeholder images.
- Cookie banner.

Known issues to address during implementation:

- The Impressum text currently references `TMG`; for Germany this should be updated to `DDG` because the German Digital Services Act replaced the old Telemedia Act framework for this context.
- The cookie banner currently has only an "accept" action. If analytics, tracking, embedded videos, maps, pixels, or marketing cookies are used, the consent flow needs a real reject/manage path.
- Legal pages should not be simple modals only. For German expectations, `Impressum` and `Datenschutzerklaerung` should be clearly reachable from every page, preferably as dedicated sections/pages or stable footer links.
- Current images are generic stock placeholders and should be replaced primarily with Tatsiana's own photos.

## 3. Reference Research Summary

### Fit mit Mareike

Reference: https://www.fitmitmareike.de

Useful patterns:

- Very clear personal brand in the hero: "FIT MIT MAREIKE".
- Main promise: achieving the client's goal together.
- Social proof via client transformations.
- Simple 3-step process: fill contact form, coach replies via WhatsApp, consultation discusses goal and price.
- Offer depth: personalized training plans, nutrition plan, progress tracking, ongoing communication.
- About/why online coaching section.
- Footer includes AGB, Datenschutz, Impressum, social links, address, phone, and email.

Takeaway for Tatsiana:

- A clear 3-step consultation process is worth using.
- The page should explain what happens after the user submits the form.
- If there are transformation photos/testimonials, they can become a strong conversion section.

### Jan Sommerstange

Reference: https://jansommerstange.de

Useful patterns:

- Main navigation: Home, Leistungen, Ueber mich, Bewertungen, Kontakt.
- Hero CTA: "Jetzt mit jan starten".
- Clear promise that the first consultation is free and non-binding.
- Simple service list: online personal training, individual training plans, exclusive consultation.
- Final CTA asks the visitor to send their current goal.
- Footer includes Impressum and Datenschutz.

Takeaway for Tatsiana:

- Keep the CTA direct and repeated.
- Ask for the visitor's current goal in the form, because it makes the first consultation easier.

### BeFitinLife

Reference: https://www.befitinlife.com

Useful patterns:

- Offer categories: Personal Training, nutrition consulting, live online group fitness.
- References/client logos and testimonials.
- About section focused on values and coaching style.
- Blog/content section for SEO.
- Footer includes Impressum, Datenschutz, AGB, Widerruf.

Takeaway for Tatsiana:

- If there are testimonials or recognizable references, include them.
- Blog is optional for the first version, but useful later for SEO.
- AGB/Widerruf may be needed if packages are sold/booked online, but may be unnecessary for a consultation-only MVP.

### Skyline Fitness

Reference: https://www.skylinefitness.de

Useful patterns:

- Clear local/online positioning.
- Experience, qualifications, services, advantages, social links.
- Pricing packages shown openly.
- FAQ section.
- Contact form includes goal, preferred contact method, source, and Datenschutz consent.

Takeaway for Tatsiana:

- FAQ should reduce common objections before the consultation.
- If prices are not final, the page can say pricing is discussed in the free consultation.
- Datenschutz checkbox should be part of the form.

## 4. Proposed Landing Page Structure

Recommended MVP sections:

1. Hero
   - Brand/name: "Tatsiana Rukhlenko".
   - Positioning: personal fitness coach / online coaching.
   - Main promise: individual training and nutrition support for realistic, sustainable progress.
   - Primary CTA: "Kostenlose Online-Beratung buchen" or "Kostenlose Beratung anfragen".
   - Strong portrait/action photo from the Google Drive folder.

2. Trust strip
   - Short signals such as experience, languages, coaching type, online availability, certifications.
   - This section depends on confirmed data.

3. Who this is for
   - Examples: fat loss, muscle tone, healthy routine, returning after a break, busy schedule, beginner-friendly training.
   - Avoid medical promises unless legally reviewed.

4. Offer / Leistungen
   - Online coaching.
   - Personal training if Tatsiana offers in-person sessions.
   - Training plans.
   - Nutrition guidance if offered.
   - Weekly check-ins / WhatsApp support if offered.

5. How it works
   - Step 1: submit form.
   - Step 2: Tatsiana contacts the user via WhatsApp/email.
   - Step 3: free online consultation.
   - Step 4: individual plan if both sides decide to continue.

6. About Tatsiana
   - Personal story, approach, qualifications, coaching philosophy.
   - Photo-led section using own images.

7. Results / Testimonials / Transformations
   - Include only if the client has permission to publish before/after photos or testimonials.
   - If not available, replace with "Coaching principles" or "What clients can expect".

8. FAQ
   - Online format.
   - Beginner suitability.
   - Training location/equipment.
   - Nutrition approach.
   - What happens in the free consultation.
   - Pricing question.

9. Final CTA / Consultation Form
   - Name.
   - Email.
   - WhatsApp or phone.
   - Goal.
   - Preferred contact method.
   - Optional message.
   - Required privacy checkbox.
   - Clear expectation: response time and next step.

10. Footer
   - Contact links.
   - Instagram / WhatsApp.
   - Impressum.
   - Datenschutzerklaerung.
   - Optional: AGB, Widerruf, Cookie settings.

Optional later sections:

- Pricing packages.
- Blog/articles for SEO.
- Corporate fitness / group classes.
- Lead magnet, for example a free PDF checklist.
- Newsletter, only if Datenschutz and email marketing consent are handled correctly.

## 5. Visual Direction

Visual thesis:

- A refined pastel fitness brand: warm skin tones, soft mint/blush/cream accents, strong real photography, clean typography, and confident spacing.

Selected working color scheme:

- Variant 2: Premium Pastel.
- Background: `#FAF7F2`.
- Required lavender: `#EDE1EF`.
- Required mint: `#D8FFF9`.
- Accent: `#B9A3C8`.
- Main text: `#26222A`.

Content plan:

- Hero creates confidence and action.
- Offer section explains what the client gets.
- About/results create trust.
- FAQ removes hesitation.
- Final form converts.

Interaction thesis:

- Smooth hero entrance for text and photo.
- Subtle scroll reveals for sections.
- Clean mobile menu and form feedback.
- No heavy animation that slows the page or distracts from booking.

Design rules for implementation:

- Use Tatsiana's real photos as the main visual asset.
- Avoid generic purple gradients, excessive cards, and decorative clutter.
- Keep the first viewport focused on name, promise, and CTA.
- Make CTA buttons visible and repeated, but not noisy.
- Ensure text contrast is strong enough on pastel backgrounds.
- Make the mobile layout feel designed, not merely stacked.

## 6. Asset Plan

Primary asset source:

- Google Drive folder supplied by the user.
- The folder currently contains many JPEG files named like `DR_260514_...jpg`.

Usage plan:

- Pick 1 strong hero image.
- Pick 1 about portrait.
- Pick 2-4 supporting action/detail photos.
- Optimize images before implementation to avoid a slow page.
- Use descriptive `alt` text in German.

Stock photo policy:

- Use Unsplash, Pexels, or Pixabay only if Tatsiana's own photo set lacks a necessary visual.
- Use only assets that are free for commercial use.
- Keep source URLs in a small attribution/asset log, even if attribution is not legally required.

## 7. Germany/EU Legal And Compliance Requirements

Important note:

- This is an implementation checklist, not legal advice. Final legal text should be generated or reviewed by a qualified German legal/privacy source.

Required or likely required:

1. Impressum
   - Required for business/commercial websites in Germany.
   - Must be easy to recognize, directly reachable, and permanently available.
   - Needs real provider data: full name/business name, address, fast electronic contact, email, and extra details depending on legal form and regulated activity.

2. Datenschutzerklaerung / Privacy Policy
   - Required because the site will process personal data at least through server access logs and likely through the contact form.
   - Must explain controller identity, processing purposes, legal basis, recipients/categories, retention, data subject rights, complaint rights, and transfer details where relevant.

3. Contact form privacy handling
   - The form should include a required checkbox confirming that the visitor has read the privacy policy.
   - The form should not ask for unnecessary data.
   - Submission destination must be known: email, WhatsApp, CRM, Formspree, custom backend, etc.

4. Cookie/consent handling
   - If the site uses only technically necessary storage, a cookie banner may not be needed.
   - If the site uses analytics, tracking pixels, embedded videos, Google Maps, third-party widgets, or marketing cookies, consent must be implemented before those tools load.
   - A good banner should include accept, reject, and settings/manage choices.

5. Health and fitness claims
   - Avoid guaranteed body transformation claims.
   - Avoid medical claims unless Tatsiana is qualified and the wording is legally reviewed.
   - Include a simple health disclaimer if advice/training plans are discussed.

6. AGB / Widerruf
   - Needed if users can buy/book paid services directly online.
   - Probably optional for consultation-only MVP, but should be revisited before adding payments or package checkout.

7. Image and testimonial permissions
   - Use only photos with permission.
   - Before/after transformation photos need explicit consent.
   - Testimonials should be published only with permission and preferably with real attribution rules agreed in writing.

Useful legal references:

- German DDG section 5: https://www.gesetze-im-internet.de/ddg/__5.html
- GDPR Article 13: https://gdpr-info.eu/art-13-gdpr/
- IHK Cologne Impressum overview: https://www.ihk.de/koeln/hauptnavigation/recht-steuern/impressum-pflichtangaben-auf-websites-5271690

## 8. SEO And Content Language

Recommended first version language:

- German, because the target market is Germany.

Potential SEO keywords:

- Personal Trainerin online
- Online Fitness Coaching
- Personal Training Deutschland
- Fitness Coach fuer Frauen
- Trainingsplan und Ernaehrung
- Kostenlose Fitness Beratung

Open question:

- Should the site be only German, or German + English/Russian?

Recommended technical SEO basics:

- Unique title and meta description.
- Real heading hierarchy.
- Descriptive image alt text.
- Open Graph image for social sharing.
- Local business schema only if real location/business details are confirmed.

## 9. Skill Candidates Found

Already available in this Codex environment:

1. `frontend-design`
   - Source: Anthropic skills.
   - Purpose: high-quality frontend visual direction and implementation.
   - Install count on skills.sh: about 427K.
   - Already available locally, no installation needed.

2. `frontend-skill`
   - Purpose: landing-page composition, imagery, hierarchy, motion, and avoiding generic card-heavy design.
   - Already available locally, no installation needed.

3. `web-design-guidelines`
   - Source: Vercel agent skills.
   - Purpose: review UI for spacing, typography, accessibility, and UX issues.
   - Already available locally, no installation needed.

Recommended optional installs before implementation:

1. `page-cro`
   - Source: `coreyhaines31/marketingskills`.
   - Purpose: conversion-rate review for landing pages: CTA clarity, trust signals, friction, objections, copy alternatives.
   - Install command:

```bash
npx skills add https://github.com/coreyhaines31/marketingskills --skill page-cro -g -y
```

2. `copywriting`
   - Source: `coreyhaines31/marketingskills`.
   - Purpose: stronger landing-page copy in German after the offer and audience are confirmed.
   - Install command:

```bash
npx skills add https://github.com/coreyhaines31/marketingskills --skill copywriting -g -y
```

3. `webapp-testing`
   - Source: `anthropics/skills`.
   - Purpose: browser/Playwright-style verification of responsive behavior and local UI flows.
   - Install command:

```bash
npx skills add https://github.com/anthropics/skills --skill webapp-testing -g -y
```

Not recommended for this project now:

- `vercel-react-best-practices`: excellent for React/Next.js, but the current project appears to be static HTML/CSS/JS. Install only if we migrate to React/Next.js.
- `deploy-to-vercel`: useful only when deployment is requested.
- `shadcn`: not needed for a static custom landing page.

Pending approval:

- The user should approve which optional skills to install before implementation.

## 10. Open Questions Before Building

### Business and positioning

1. What is Tatsiana's exact title in German: `Personal Trainerin`, `Fitness Coach`, `Online Fitness Coach`, or something else?
2. Is the target audience mostly women, men, beginners, busy professionals, mothers, athletes, or general clients?
3. What is the main niche: weight loss, muscle building, body recomposition, posture, strength, healthy habits, post-pregnancy, mobility, or general fitness?
4. What makes Tatsiana different from other coaches?
5. How many years of experience does Tatsiana have?
6. Does she have certifications, licenses, education, or competition experience that should be shown?
7. Which languages can she coach in: German, English, Russian, Belarusian, Polish, other?

### Services

8. Does Tatsiana offer online coaching only, or also in-person training?
9. If in-person training exists, in which city/area in Germany?
10. Does she provide nutrition coaching?
11. Does she provide meal plans, or only nutrition guidance?
12. Does she provide gym plans, home workout plans, or both?
13. Does she use an app for coaching, PDF plans, WhatsApp, Google Sheets, Trainerize, Lenus, or another platform?
14. Are weekly check-ins included?
15. Does she offer group classes or only 1:1 coaching?

### Conversion flow

16. What should happen when someone submits the consultation form?
17. Should the CTA open WhatsApp directly, send email, submit a form, or link to Calendly/booking software?
18. Do you want Calendly or another booking tool embedded?
19. What is the expected response time: 24 hours, 24-48 hours, same day?
20. Should the consultation be called free, non-binding, or both?
21. Should we ask for phone/WhatsApp number as required or optional?
22. Which fields should be required in the form?
23. Should the form include preferred contact method?
24. Should the form include current fitness goal?
25. Should the form include current training level?

### Content and proof

26. Do you have testimonials from clients?
27. Do you have permission to publish testimonials with names/photos?
28. Do you have before/after transformation photos?
29. Do you have permission to publish transformation photos?
30. Do you want to show prices/packages, or discuss pricing only during the consultation?
31. Do you want a FAQ section?
32. Do you want a blog section now, or later?
33. Should the tone be friendly and warm, premium and minimal, energetic and bold, or soft and supportive?

### Legal data

34. What is the legal business name for Impressum?
35. What is the full business address?
36. What email should be shown in Impressum?
37. What phone number should be shown, if any?
38. Is there a VAT ID / USt-IdNr.?
39. Is Tatsiana a sole proprietor/freelancer or a company?
40. Are there professional licenses or supervisory authority details that must be listed?
41. Will the site use analytics, such as Google Analytics, Plausible, Fathom, or Vercel Analytics?
42. Will the site use Meta Pixel, TikTok Pixel, Google Ads, or other marketing tracking?
43. Will the site embed Instagram, YouTube, Google Maps, Calendly, WhatsApp widgets, or other third-party tools?
44. Who will provide final Datenschutz and Impressum text?

### Design and assets

45. Which photos from the Google Drive folder do you prefer for the hero?
46. Are there any photos that must not be used?
47. Should the design use mostly blush/pink pastel, mint pastel, cream/white, or another palette?
48. Do you already have a logo?
49. If no logo exists, should we use a clean text logo?
50. Should the brand name be `Tatsiana Rukhlenko`, `TR Fitness`, or another name?
51. Should the website feel more feminine, neutral, athletic, luxury, or clinical/credible?

### Technical scope

52. Should we keep the project as static HTML/CSS/JS?
53. Should we migrate to React/Next.js?
54. Where will the website be hosted?
55. Do you need deployment now or only local files?
56. Do you need a real backend for the form, or is a mailto/WhatsApp flow enough for the first version?
57. Do you want the site to support multiple languages?
58. Do you want cookie settings to be editable after the user makes a choice?

## 11. Recommended Decisions For MVP

Recommended MVP assumptions if the user wants fast progress:

- Static HTML/CSS/JS is enough for the first version.
- Language: German only.
- Main CTA: free non-binding online consultation.
- Form fields: name, email, WhatsApp/phone, goal, preferred contact method, message, privacy checkbox.
- Use own photos first; avoid stock unless a visual gap appears.
- No analytics in the first version unless explicitly requested. This reduces cookie consent complexity.
- No pricing table until the offer is confirmed.
- Include Impressum and Datenschutz as dedicated reachable legal content with placeholders clearly marked until real legal text is provided.
- Include FAQ and 3-step process because they directly support conversion.

## 12. Next Step

Before implementation, the user should answer:

1. Which optional skills should be installed: `page-cro`, `copywriting`, `webapp-testing`, all, or none?
2. Which sections are approved for MVP?
3. Which contact/booking flow should be used?
4. Which legal data can be provided now, and which should remain placeholders?
5. Should the first implementation keep static HTML/CSS/JS or migrate to another stack?
