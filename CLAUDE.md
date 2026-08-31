# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A YAML-driven resume generator. Content lives in YAML, presentation lives in layout
configs, and three separate renderers turn the two into HTML. Built for Jonathan
Crissey's resume; the culinary resume shares the same machinery.

## Repository layout

Flat. There is no `js-render/` or `python-build/` directory — earlier versions of this
file described a split that never existed.

```
resume-data/
  resume-data.yml            # tech resume (primary)
  culinary-resume-data.yml   # culinary resume
layout-config.yml            # two-column professional (the default everywhere)
layout-modern.yml            # two-column, larger type
layout-creative.yml          # two-column, header in sidebar
layout-minimal.yml           # SINGLE COLUMN - use this for ATS submissions
cover-letter.yml             # DataAnnotation.tech cover letter (draft, not rendered yet)
index.html                   # primary renderer - this is what `/` serves
resume-viewer.html           # older renderer, partially stale (see below)
build_resume.py              # static generator
flower-of-life.js            # print-time profile image replacement
jc_resume.html               # the original static resume, kept for reference
```

## The three renderers, and why that matters

**Rendering logic is duplicated across three files.** This is the single most important
thing to know about this repo. `index.html`, `resume-viewer.html`, and `build_resume.py`
each carry their own copy of the section-rendering `if/else` chain.

- **`index.html`** — the primary renderer, served at `/`. Resume dropdown is populated
  from a hardcoded `resumeFiles` array near the bottom of the file. All four layouts are
  in the layout dropdown. **Edit this one first.**
- **`resume-viewer.html`** — older. Its resume dropdown still lists `resume-data-2.yml`,
  which does not exist, and its layout dropdown offers only `layout-config.yml`. Kept
  working but not the one to demo from.
- **`build_resume.py`** — prompts for which resume to build, then **hardcodes
  `layout-config.yml`**. It cannot currently produce the other layouts. Writes
  `<resume-name>.html` (e.g. `resume-data.html`), which is gitignored.

Consequence: **adding one section means editing five files** — the data YAML, each layout
that should show it, and all three renderers. Forgetting a renderer produces a section
heading with an empty body, which is exactly what happened when `ai_engineering` was
added to `resume-viewer.html` but not `index.html`.

`REFACTOR-DYNAMIC-SECTIONS.md` (parked on `feature/culinary-favorite-dishes`, see
Branches) proposes fixing this. See "Planned work" below.

## Section shapes

A section's renderer branch is chosen by its **name**, but every section really falls into
one of six shapes determined by its keys. This is the basis for the proposed refactor.

| Keys | Sections |
|---|---|
| `content` | profile, algorithm, availability |
| `items` | interests, favorite_dishes |
| `content` + `highlights` | ai_engineering |
| `categories` | skills |
| `jobs` | experience |
| `degrees` | education |

`header` and `contact` are special-cased in every renderer because they read from
`personal:` rather than `sections:`.

Current sections in `resume-data.yml`: profile, ai_engineering, experience, education,
skills, interests, algorithm.

## Gotchas that have cost real debugging time

- **The controls bar overlays the end of the page.** `.controls` is
  `position: fixed; bottom: 0`. `body` now carries `padding-bottom: 160px` to reserve
  space (removed under `@media print`). Without it the last section on the page — usually
  Interests — is hidden behind the bar and looks like a rendering failure.
- **Check which file the browser is actually loading.** `GET /` is `index.html`, not
  `resume-viewer.html`. `index.html` also pulls `flower-of-life.js`; `resume-viewer.html`
  does not. The server access log settles this instantly.
- **YAML fetches are cache-busted** (`cache: 'no-store'` plus a timestamp) in both HTML
  renderers, so data edits show up on reload. The HTML files themselves can still be
  browser-cached.
- **`layout-minimal.yml` has no `sidebar` key.** Renderers must not assume one exists.

## Development commands

```bash
# Live preview (primary renderer at /)
python3 -m http.server 8000

# Static build - prompts for which resume, always uses layout-config.yml
pip install -r requirements.txt
python3 build_resume.py
```

## Content

Resume sections: contact and profile image, profile, AI-assisted engineering, experience
(18 years, primarily IBM), education (B.S. Computer Science, UTSA 2007), skills,
interests, and a flower-of-life algorithm easter egg.

Skills categories, in order:

- AI-Assisted Engineering
- Systems & Applications
- Cloud & Infrastructure Engineering
- Application Development
- Security & Compliance

### Writing conventions for resume prose

Learned the hard way while drafting the AI section and cover letter:

- **No product or model names** in the AI section — describe techniques, not tooling.
- **Describe techniques, not projects.** The section is about how the work is done.
- **Say things once.** Repeating a concept across bullets reads as padding.
- **Verify every number before writing it.** Commit-trailer counts measure commit-message
  policy, not AI usage — two repos explicitly forbid `Co-Authored-By`. Counting
  `CLAUDE.md` files across `~/working` includes forks that aren't ours.
- **Cover letter voice**: at most one "I" per paragraph, never in consecutive sentences,
  minimal em-dashes, no "I'll be direct about" style throat-clearing.

## Branches

- `feature/culinary-favorite-dishes` — parked. Adds `favorite_dishes` to the modern and
  creative layout sidebars, plus `REFACTOR-DYNAMIC-SECTIONS.md` and a scratch debug page.
  Not merged: `favorite_dishes` only exists in the culinary data, so wiring it into shared
  layouts is the coupling the refactor doc argues against.
- `feature/styling-templates` — stale. Zero commits ahead of `main`, 13 behind. Safe to
  delete.

## Planned work

### Dynamic section rendering (next up)
Dispatch on section **shape** rather than name — six handlers per renderer replacing ~31
name-specific branches. No data changes needed; shape is inferred from which keys a
section has. Verify by diffing rendered HTML before and after; byte-identical output means
the refactor is correct. `header` and `contact` stay special-cased.

### Cover letter rendering
`cover-letter.yml` exists but nothing renders it. Needs a letter layout plus a combined
page that prints the letter followed by the single-column resume, with a page break
between, so `Print → Save as PDF` produces one file for job applications.

### ATS considerations
Use `layout-minimal.yml` for anything submitted through an applicant tracking system.
Two-column layouts with a sidebar are frequently mangled — read straight across, or the
sidebar dropped entirely, which would lose the entire skills block.

### Web-based editor (someday)
`resume-editor.html` to edit YAML through a form, with backups on save and live preview.
Note the sibling `project-home` repo removed exactly this kind of generator tooling after
its output proved less precise than hand-curation.
