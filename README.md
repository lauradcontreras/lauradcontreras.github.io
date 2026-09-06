# lauradcontreras.github.io

Personal academic site. Plain Jekyll — GitHub Pages builds it natively from `master`,
so there is no Actions workflow and no `gh-pages` branch to keep in sync.

## Where things live

| To change | Edit |
| --- | --- |
| Name, role, affiliation, email, CV link, social links (sidebar) | `_config.yml` |
| The sidebar order of nav items | `_data/nav.yml` |
| All layout and styling (one file, CSS inline) | `_layouts/default.html` |
| Bio | `index.md` |
| Papers | `research.md` |
| Teaching | `teaching.md` |
| CV page | `cv.md` |
| CV PDF | `assets/pdf/contreras_CV.pdf` |
| Portrait | `assets/img/prof_pic.jpg` |
| Paper figures | `assets/fig/` |

## Adding a paper

Copy an existing `<div class="paper" markdown="1">` block in `research.md`. The pieces:

- `{: .paper__title}` — the title line
- `{: .paper__authors}` — authors; wrap your own name in `<span class="me">`
- `{: .paper__note}` — small uppercase status line ("Draft available upon request")
- `<details><summary>Abstract</summary>` — collapsible panel
- `{: .paper__links}` — the row of links at the bottom

## Adding a figure to a paper

Put two images in `assets/fig/`: a context image and the results figure. Then uncomment
the `<div class="fig">` block in that paper. The context image shows by default and the
results figure fades in on hover. One image alone also works — drop the `.alt` line.

## Previewing

`python3 _preview.py` renders approximate HTML into `_preview/` without Ruby. It handles
only the small Liquid subset this layout uses — good enough to check design, not a
substitute for a real Jekyll build.
