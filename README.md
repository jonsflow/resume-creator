# Resume Creator

A modular resume generation system that builds professional resumes from YAML content and
swappable layout configurations.

## Quick Start

```bash
python3 -m http.server 8000
```

Open http://localhost:8000 — pick a resume and a layout from the dropdowns, then use
Print Resume to save a PDF.

For a static, self-contained file instead:

```bash
pip install -r requirements.txt
python3 build_resume.py
```

It prompts for which resume to build and writes `<resume-name>.html` (for example
`resume-data.html`) with CSS embedded. Note that it always uses `layout-config.yml`.

## File Structure

```
resume-data/                 your resume content
  resume-data.yml
  culinary-resume-data.yml
layout-config.yml            two-column professional (default)
layout-modern.yml            two-column, larger type
layout-creative.yml          two-column, header in sidebar
layout-minimal.yml           single column
cover-letter.yml             cover letter content
index.html                   main renderer (served at /)
resume-viewer.html           older renderer
build_resume.py              static generator
IMG_4428.jpeg                profile image
```

## Layouts

Content and presentation are fully separated, so the same resume data renders through any
layout. A layout config controls colors, typography, spacing, and which sections appear in
which column.

`layout-minimal.yml` is single-column. Prefer it for applications submitted through an
applicant tracking system — multi-column layouts are often parsed incorrectly, and a
dropped sidebar takes the whole skills section with it.

## Creating a New Layout

1. Copy an existing layout config to a new name
2. Adjust `colors`, `typography`, `spacing`, and the `layout.structure` section lists
3. Add it to the layout dropdown in `index.html`

Every section named in `structure.sidebar.sections` or `structure.main.sections` must have
a matching renderer branch, or it will render as a heading with nothing beneath it.

## Adding a Section

Rendering logic is currently duplicated across `index.html`, `resume-viewer.html`, and
`build_resume.py`, so a new section type needs a branch added in each. See `CLAUDE.md` for
the section shapes and the planned refactor that would remove this duplication.
