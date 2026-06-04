# Design System

This file documents the visual rules for the Tatsiana Rukhlenko landing page.
It is intentionally simple because the project is a static HTML/CSS/JS website.

## Design Direction

The brand should feel calm, precise, and warm.

The page should stay pastel-card based, but it must not feel like a cheap generic fitness template. Real trainer photos, clear mobility language, and careful spacing should do more work than decorative elements.

Avoid:

- aggressive gym or bodybuilding visuals;
- medical pain-cure promises;
- fake urgency, before/after pressure, or loud transformation copy;
- too many identical icon cards in a row;
- legal placeholders inside the main conversion path.

## Color Tokens

Use the existing CSS variables in `style.css` as the single source of truth.

| Token | Value | Use |
|---|---:|---|
| `--color-bg` | `#FAF7F2` | Page background and soft icon circles |
| `--color-lavender` | `#EDE1EF` | Soft brand surface, about section, gentle emphasis |
| `--color-mint` | `#D8FFF9` | Fresh accent surface, contact and offer emphasis |
| `--color-accent` | `#B9A3C8` | Small highlights, focus rings, supporting accents |
| `--color-text` | `#26222A` | Primary text |
| `--color-muted` | `#62586A` | Secondary text |
| `--color-line` | `rgba(38, 34, 42, 0.12)` | Dividers and quiet borders |
| `--color-white` | `#FFFFFF` | Cards and form surfaces |
| `--color-deep` | `#211D26` | Dark CTA and consultation section |

## Typography

- Font stack: `Avenir Next`, `Segoe UI`, Helvetica, Arial, sans-serif.
- Do not load external font files in the MVP.
- Headings should be large, calm, and readable.
- Avoid negative letter spacing.
- Use sentence-style labels more often than tiny uppercase section eyebrows.
- Keep body text comfortable, usually below 75 characters per line.

## Layout

- Main container: `--container: 1160px`.
- Mobile gutters should keep the page inside the viewport. No horizontal scroll.
- Use CSS Grid for multi-column sections and switch to one column on mobile.
- Let the first viewport show the hero and a hint of the next section.
- Use real photos as trust anchors, especially in hero and about sections.

## Components

### Buttons

- Primary buttons use dark background and white text.
- Secondary buttons use a light surface and a quiet border.
- Buttons should have visible hover, focus, and active states.
- Button text should describe the action, for example `Beratung anfragen` or `Prepare email`.
- On mobile, the primary consultation action may stay reachable in a compact bottom bar until the visitor reaches the form.

### Cards And Tiles

- Pastel-card style is approved.
- Cards should feel soft and calm, not like a repeated template.
- Do not pair a visible 1px border with a very large soft shadow on the same card.
- Use rounded corners, but avoid over-rounding cards.
- Use hover lift and a small zoom only when it helps the user understand interactivity or focus.

### Forms

- Every input needs a visible label.
- Required fields use native HTML validation.
- The MVP form uses `mailto:` and must explain that no data is stored on the website.
- Always provide a direct email fallback near the form.

### Legal

- Impressum and privacy information must be reachable from the footer.
- Detailed legal placeholders belong on the legal page, not inside the main marketing flow.
- Use DDG wording, not deprecated TMG wording.
- The final legal text must be reviewed before public launch.

## Motion

- Motion should be subtle: hover lift, small zoom, and gentle reveal.
- Content must remain readable if JavaScript does not run.
- Respect `prefers-reduced-motion`.
- Do not animate layout properties such as width, height, margin, or padding.

## Bilingual Rules

- German and English content must cover the same visible sections.
- New visible text needs a `data-i18n` key and matching translations in `script.js`.
- The selected language is stored in `localStorage` as `preferredLanguage`.
- Legal pages should open in the language selected on the main page.

## QA Checklist

- Desktop and mobile layouts have no horizontal overflow.
- DE/EN switching updates all visible text.
- The consultation form validates required fields.
- The mailto message contains name, email, goal, message, and privacy confirmation.
- No analytics, pixels, third-party widgets, Google Fonts, or cookie banner are loaded.
- Footer legal links work.
