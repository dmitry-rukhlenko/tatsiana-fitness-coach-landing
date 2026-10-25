# Tatsi in motion — 10 SVG logo concepts

Date: 25 October 2026. Status: concepts for the owner's visual selection.

## Approved brief

Create ten distinct, simple, elegant, recognizable logos for a fitness coaching
business focused on freedom of movement, strength and mobility. Use white
`#ffffff` and mint `#bcf7f3`. The full name is optional: T, TM, a word or an
abstract mark may carry the idea. Save each concept separately as editable SVG.
The user's request also authorizes installing a missing logo/SVG design skill.

## Delivery and checks

- Ten self-contained SVG files, transparent backgrounds, editable vector shapes.
- No bitmap images, external fonts, external resources or scripts in the logos.
- Numbered visual comparison, local gallery and ZIP of the ten master SVGs.
- Parse all files, verify palette, inspect rendered geometry and preview at small sizes.
- The dark presentation surface is not part of the exported logos.
- Owner selection and visual acceptance remain pending.
- Follow-up authorized in this same chat: show each of the ten concepts on a
  website and Instagram. Deliver ten comparison boards plus separate website
  and Instagram preview images. Reuse the site's existing photos and copy in
  explicitly labelled local mockups; no posting or changes to a live account.

This is a Local design task: new, reversible artifacts in one output folder.
No edits to the website, existing designs or original photos; no publication.
The pre-existing untracked `.claude/` folder belongs to earlier work.

## Skills

- Brainstorm: ten independent visual concepts within the supplied brief.
- find-skills: locate and inspect a bounded SVG logo skill.
- SVG Logo Designer, rknall/claude-skills: editable SVG organization, geometry,
  scalability and concept presentation. Installed in the personal Codex skills
  directory under the user's explicit request. Its generic quantity and palette
  defaults are superseded by the ten concepts and exact colors requested here.

Source: https://github.com/rknall/claude-skills/tree/main/svg-logo-designer

## Checkpoint

Technical preparation complete: ten SVG masters, ten HTML context boards,
thirty PNG application previews, two galleries and two ZIP archives. The SVG ZIP
matches all masters byte for byte; the full preview ZIP has 42 verified entries.
All sixty logo placements have identical shape/color attributes to their masters.
Fresh local browser checks passed with no clipped logos, missing images,
console errors, remote requests or gallery overflow at 1440 and 390 px.
The ten master designs, all website/avatar placements, representative full
context boards including both wordmarks, and mobile galleries were visually
inspected. The long-screenshot rendering issue was resolved with viewport
captures. Wordmarks 06 and 09 are visibly less legible in small round avatars.
Evidence: verification.json, applications-verification.json,
gallery-verification.json and preview/.
Website files and pre-existing .claude/ state are unchanged. New design files
remain uncommitted. Human selection/visual acceptance is pending.
Next: owner selects a direction or requests revisions to named concepts.

Follow-up: the applications gallery now shows one panel at a time. Mouse hover
over a numbered tab selects it immediately; click/tap and keyboard navigation
also work. Direct links such as #concept-08 preserve their selection without
scrolling past the selector. Generator updated to preserve this behavior.
Offline execution of applications.js verified all ten hover selections, a
single visible panel, selected styling attributes, touch clicks, arrow/Home/End
handling and hash selection. All ten SVG hashes remain unchanged.
Fresh visual verification of this interaction was blocked because Browser Use
does not permit file:// URLs. The user's open tab was not refreshed or operated.

## Extension: concepts 11-20 (Claude set), 25 October 2026

The owner asked for a second, independent set and for the same website and
Instagram mockups on this page. Claude's ten geometric concepts (masters in
`../logo-concepts-2026-10-25-claude/`) were copied into `svg/` as `11-…`
to `20-…`, unchanged. `build-applications-11-20.py` builds their boards on the
same template as `build-applications.py` and appends tabs/cards 11-20 to
`applications.html` and `index.html`; `render-applications-11-20.cjs` renders
the PNGs with a stroke-aware clipping check (`applications-verification-11-20.json`).
Both ZIP archives now also carry 11-20. Files 01-10 and their scripts are
unchanged. Owner selection remains pending.

## Extension: concepts 21-30 (calligraphic / Didone set), 25 October 2026

After seeing reference images (thin mint flourishes, open rings, a script or
Didone t/T in dark ink on white), the owner asked for ten more in that style.
`build-21-30.py` outlines letterforms from macOS system fonts (Snell Roundhand,
Zapfino, Didot) with fontTools via `glyphs.py`, draws tapered mint flourishes as
filled paths and writes `svg/21-…30-…` plus `concepts-21-30.json`. On white the
mint is one step deeper (#86e3da) because #bcf7f3 is 1.2:1 against white; the
mockups swap it back to #bcf7f3 and the ink to white on dark surfaces
(`on_dark` map). The gallery builder/renderer now take the concepts file as an
argument. Font licences: Apple system fonts are licensed for use on macOS;
commercial logo use of the outlines should be checked before final delivery.
