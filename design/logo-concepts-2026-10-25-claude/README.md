# Tatsi in motion — 10 logo concepts (Claude set)

Date: 25 October 2026. Status: concepts for the owner's visual selection.
A second, independent set made by Codex the same day lives in
`../logo-concepts-2026-10-25/` (script / figurative direction). This set is
geometric and constructed, so the two sets do not repeat each other.

## Brief

Simple, elegant, recognizable logo for a fitness coaching business about moving
freely, strength and mobility. Colours: white `#ffffff` and mint `#bcf7f3`.
The full name is optional: a letter, initials or a word may carry the idea.

## Files

`svg/` — ten separate master files, transparent background, only the two brand
colours, no text elements, no fonts, no rasters, no filters. Every shape is a
plain `<path>` or `<circle>` with an `id`, so each part can be edited in
Illustrator, Figma, Inkscape or by hand. Canvas 256×256 (wordmark 640×256).

| # | File | Idea in one sentence |
|---|---|---|
| 01 | `01-swing-t.svg` | T whose crossbar is a swinging arc; the mint dot is the moving end. |
| 02 | `02-ti-lean.svg` | "ti" (Tatsi / in motion) leaning 15° forward, the i-dot running ahead. |
| 03 | `03-open-ring-t.svg` | A mint ring open at the bottom; the T steps out through the opening. |
| 04 | `04-joint.svg` | Ball-and-socket joint: a mint ball moving freely in a white socket. |
| 05 | `05-lift-t.svg` | T whose right half of the crossbar lifts like a rising arm. |
| 06 | `06-tatsi-wave.svg` | Geometric wordmark "tatsi"; one mint wave is the crossbar of both t's. |
| 07 | `07-split-disc-t.svg` | A disc cut by two gaps; the gaps form the T (negative space). |
| 08 | `08-thread.svg` | A mint ribbon flowing freely through a white ring (the body). |
| 09 | `09-rocker-t.svg` | A white T balanced on a mint rocker: stable, yet able to move. |
| 10 | `10-supple-t.svg` | T with a supple spine: straight crossbar, S-curved stem. |

`preview/contact-sheet.html` / `.png` — all ten on the dark surface at large
size plus true 64 / 32 / 16 px renders.
`preview/test-sheet.html` — the logo-design skill's test sheet (size ladder,
pixel test, backgrounds, one-colour, blur, mirror, favicon and header contexts).

## Notes for editing and production

- The marks are stroke-based (round caps), so each weight is one number per
  element (`stroke-width`). Before print or cutting, expand strokes to outlines
  in a vector editor (Illustrator: Object → Expand; Inkscape: Stroke to Path).
- White on a transparent background is invisible on light surfaces; that is
  inherent to the brief. For light backgrounds swap `#ffffff` for the site's
  dark `#211D26`, or export one-colour versions with the skill's
  `export_variants.py --mono`.
- The wordmark (06) is the only concept that does not survive 16 px; use a
  symbol for favicons.

## Verification

- `svg_audit.py` from the logo-design skill: every file parses, uses exactly
  two colours, has no text / raster / filter; scores 97–100 / 100 (heuristic).
- Rendered via headless Chrome and inspected visually at 512 px and at
  64 / 32 / 16 px (`preview/contact-sheet.png`), plus the skill's test sheet
  (one-colour, reversed, pixel test, mirror / rotate).
- Owner selection and visual acceptance are pending. No trademark search was
  made.

## Skills used

- `find-skills` — located candidates on skills.sh.
- `logo-design` (kaankiziltug/logo-design-skill, installed to
  `~/.claude/skills/logo-design`): construction rules, `svg_audit.py`,
  `preview_sheet.py`, `render_png.py`.
