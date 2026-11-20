# Adventure Builder — Software Architecture Document

A local static edition of the Adventure Builder architecture document and its two
view and interface templates. Original authors: **Paulo Merson and Darpan Saini**,
Software Engineering Institute / Carnegie Mellon University. The material
accompanies *Documenting Software Architectures: Views and Beyond, Second Edition*
(2010).

Open **[index.html](index.html)** in your browser. Navigation, search and diagrams
also work directly from disk, without a server, installation or Internet access.
External bibliographic links require a connection and retain their historical
source addresses; their current availability has not been verified.

## Organization

```text
index.html                      Entry point and reading paths
architecture/
  roadmap.html                  Document scope and organization
  system-overview.html          Functionality and quality attribute requirements
  reading-guide.html            Guide to views and templates
  documentation-status.html     Gaps already present in the source
  views/
    modules/                    Dependencies, decomposition, workflow and data
    runtime/                    SOA, Consumer Website and OPC
    allocation/                 Deployment and installation
  interfaces/                   Purchase order and order tracking
  crosscutting/                 View mappings and requirements traceability
  reference/                    Glossary, bibliography and authors’ notes
templates/                     The two browsable templates
assets/
  css/                          Shared styles, responsive layout and printing
  js/                           Local search and mobile contents menu
  diagrams/                     Relevant diagrams, without duplicates
  downloads/                    Available Visio files and Markdown templates
content/                        Editable content using the same directory tree
  pages.json                    Titles, descriptions, groups and navigation order
  migration.json                Mappings from the original pages
scripts/
  build_site.py                 Generator using only Python’s standard library
  validate_site.py              Local link, fragment and resource checks
```

## Maintenance

Edit the HTML fragments in `content/`, keeping links relative to the corresponding
published page. Edit `content/pages.json` to change titles, descriptions or
navigation. Files in `architecture/`, `templates/` and `index.html` are generated;
do not edit them directly.

Rebuild and validate from the project directory with **Python 3.9 or later**:

```bash
python3 scripts/build_site.py
python3 scripts/validate_site.py
```

Downloadable Markdown templates are in `assets/downloads/`. When changing the
HTML template instructions, also update these two files.

For an optional HTTP preview:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000`. To host the site on a static server, copy
`index.html`, `architecture/`, `templates/` and `assets/`, preserving their relative
directory structure. No compilation, external services or routing rules are
required.

## GitHub Pages

The repository workflow `.github/workflows/adventure-builder-pages.yml` rebuilds
and validates this site, then publishes only `index.html`, `architecture/`,
`templates/` and `assets/`. Source fragments, scripts and the repository's other
projects are not included in the Pages artifact.

In the repository's **Settings → Pages → Build and deployment**, set **Source**
to **GitHub Actions**. Commit and push the workflow to `main`. Later pushes that
change `adventure-builder/` or the workflow automatically publish a new version;
you can also run **Publish Adventure Builder** manually from the **Actions** tab
on `main`.

The contents of this directory are published at the site's root:
<https://niccap.github.io/architectures/>.

## Editorial approach

All site content, navigation, introductory guides and project documentation are
in English. The remaining diagrams, original specifications, TODOs and TBDs are preserved: this
reorganization neither completes nor updates the historical architecture.

The 2005 Java Pet Store example, the old SAD template and related pages, reflections
from the old exercise, duplicates and Confluence service pages have been removed.
Empty Adventure Builder pages are summarized in the documentation status page.

See [MIGRATION.md](MIGRATION.md) for details of the reorganization.
