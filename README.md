# lauradcontreras.github.io

Personal academic website of Laura Contreras-Portela, built with [Jekyll](https://jekyllrb.com/) and the [al-folio](https://github.com/alshedivat/al-folio) theme.

## Where things live

| What you want to change | File |
| --- | --- |
| Bio, photo caption, job-market line | `_pages/about.md` |
| Section headings on the research page | `_pages/publications.md` |
| Job market paper | `_bibliography/jmp.bib` |
| Working papers | `_bibliography/working.bib` |
| Work in progress | `_bibliography/wip.bib` |
| Teaching | `_pages/teaching.md` |
| CV content (rendered page) | `_data/cv.yml` |
| CV PDF | `assets/pdf/contreras_CV.pdf` |
| News items on the homepage | `_news/announcement_*.md` |
| Email, X, GitHub, Scholar links | `_data/socials.yml` |
| Co-author links | `_data/coauthors.yml` |
| Site title, URL, feature switches | `_config.yml` |
| Profile photo | `assets/img/prof_pic.jpg` |

## Adding a paper

Add a BibTeX entry to the relevant file in `_bibliography/`. Useful fields:

- `abstract` — adds an expandable "Abs" button
- `pdf` — adds a "PDF" button (a bare filename is looked up in `assets/pdf/`)
- `html` / `website` — adds a link button
- `abbr` — a coloured tag to the left of the entry (colours are set in `_data/venues.yml`)
- `selected = {true}` — also shows the paper on the homepage
- `note` — a short line under the title, e.g. `Draft available upon request`
- `additional_info` — free markdown appended after the entry (used here for presentation lists)

## Publishing

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site and pushes the
result to the `gh-pages` branch. GitHub Pages must be set to serve from `gh-pages` / `(root)` under
**Settings → Pages**.

## Previewing locally

With Docker:

```bash
docker compose up
# then open http://localhost:8080
```

Or with a local Ruby toolchain:

```bash
bundle install
bundle exec jekyll serve
# then open http://localhost:4000
```
