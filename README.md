# Nazmul Haque Turja — academic portfolio

A static site with no runtime dependencies, JavaScript, remote fonts, or tracking.
The generated HTML works on GitHub Pages and can also be opened directly.

## Edit content

Edit the JSON files in `content/`, then run:

```sh
python3 scripts/build.py
python3 scripts/check_links.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Preview at http://127.0.0.1:8000. Commit the content files **and generated HTML**
when publishing. No Node installation or package download is needed to build.

| File | What to edit |
| --- | --- |
| `content/profile.json` | Name, affiliation, PhD focus, current work, contact links, research areas, CV path |
| `content/publications.json` | Citations, paper/code/slides links, homepage selections |
| `content/projects.json` | Project status, problem, contribution, methods, outcomes, links |
| `content/updates.json` | Dated news; the four newest items appear on the homepage |
| `content/cv.json` | Education, appointments, skills, coursework, awards |
| `templates/base.html` | Shared navigation, metadata, and footer |
| `assets/site.css` | Responsive layout, typography, focus states, and print styles |
| `scripts/build.py` | Page composition; ordinary content changes do not require editing this |

### Add a publication

Append an object to `content/publications.json`. Publications are sorted by year,
author names are rendered consistently, and the owner's name is emphasized.
BibTeX downloads and disclosure panels are generated from the same record.

```json
{
  "id": "unique-paper-2026",
  "year": 2026,
  "type": "Conference paper",
  "title": "Paper title",
  "authors": ["Nazmul Haque Turja", "Another Author"],
  "venue": "Full conference or journal name",
  "summary": "One sentence explaining the work.",
  "links": [
    {"label": "Paper", "url": "https://example.org/paper"},
    {"label": "Code", "url": "https://github.com/owner/repository"},
    {"label": "Slides", "url": "pdf/slides.pdf"}
  ],
  "featured": true
}
```

Only add actual links. An empty `links` array is supported. IDs must be unique
and use lowercase letters, numbers, and hyphens. Use `featured: true` for the
homepage. Cite the authors and year of the linked version.

### Add a project

Append to `content/projects.json`. Available categories are `ongoing`, `research`,
`engineering`, and `iot`. Use the existing entries as examples.

```json
{
  "id": "unique-project",
  "title": "Project title",
  "category": "ongoing",
  "status": "Ongoing",
  "summary": "One sentence describing the work.",
  "problem": "The question or problem being addressed.",
  "contribution": "What I personally contributed.",
  "methods": "Methods actually used, or explicitly marked as planned.",
  "result": "Current stage; do not present planned outcomes as completed.",
  "links": []
}
```

Blank fields are omitted from the page. For ongoing work, `result` is presented
as **Current status**.
Framework repositories are labeled as frameworks, not as paper-specific code.

### Add an update

```json
{
  "date": "2026-10-01",
  "display_date": "Oct 2026",
  "text": "A short update. Mark future appointments as upcoming until they begin.",
  "link": {"label": "More details", "url": "projects.html#project-id"}
}
```

The `link` is optional. Updates are sorted by ISO date, newest first.

## CV download

`pdf/Nazmul_Turja_CV_2026.pdf` is the current website CV, generated from the print
layout of `cv.html`. After changing CV content, rebuild and print `cv.html` to PDF
from a browser (A4, approximately 16 mm margins); replace that file. The original
`pdf/Resume_Nazmul_September_2026.pdf` is retained as a source document and is not
the site's current download. It has the older location/affiliation.

## Review and publishing

- `python3 scripts/check_links.py` checks local assets and page fragments.
- `python3 scripts/check_links.py --external` additionally requests all public
  links with curl and writes `docs/link-audit.json`. Network access is required.
  A blocked automated request does not prove that a link is broken.
- Review `docs/content-review.md` for remaining bibliographic/date questions.
- Browser screenshots and automated accessibility results are in `docs/preview/`.
- Existing `index.html`, `research.html`, `publications.html`, `contact.html`,
  `teaching.html`, and `Sp20.html` URLs remain usable.
- Old unrelated template pages redirect to the appropriate current page.
- Old jemdoc sources are preserved in `archive/legacy-jemdoc/` for reference;
  they no longer generate the site. Do not rebuild from that directory.

Changes are local until committed and published through the repository's normal
hosting workflow.
