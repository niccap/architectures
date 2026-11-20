# Reorganizing the download

The original download was a recursive Confluence mirror: 369 HTML documents,
wiki product resources, service pages and attachments for two different examples.
The result is a static site with **24 pages**, **10 views**, **2 interface contracts**
and **2 templates**. It retains 20 distinct raster diagrams and 9 Visio files,
plus two Markdown outlines derived from the templates.

## Preserved content

- Roadmap, system overview, functionality and quality attribute requirements.
- Module, component and connector, data, deployment and installation views.
- Specifications for `OpcPurchaseOrderService` and `OpcOrderTrackingService`.
- View mappings and the requirements traceability matrix, including TODOs.
- The Adventure Builder glossary and relevant bibliography.
- Notes on the document’s educational purpose, attribution and source limitations.
- View and interface templates based on the second edition of the book.

## Removed material

- The 2005 Java Pet Store SAD, all its views, glossary, roadmap and attachments.
- The 2005 Software Architecture Documentation Template and all its subpages,
  including the XML variant, while retaining the two more recent templates.
- Reflections from the old exercise and Pet Store-specific bibliographic references.
- Confluence history, diff, metadata, reordering and attachment management pages.
- Wiki menus, login, remote search, Confluence scripts, fonts, icons and styles.
- The old entry-point redirect and `wget.sh` script.
- The soapatterns.org notation diagrams in the Top Level SOA and OPC runtime views,
  together with their notation legend links.

Pages duplicated by title and `pageId` have been consolidated. `Po int spec` and
old links to `PurchaseOrder Interface Spec` now resolve to the more complete
`OpcPurchaseOrderService` specification. The actual view mapping is from the
`MappingBetweenViews` page; `Mapping Between Views` contained generic introductory
text and placeholders.

## Gaps in the source

Implementation View, Adventure Architecture Background and WebServiceBroker
Interface Documentation were empty or contained only TODO. Their destinations
are now explicit sections of `architecture/documentation-status.html`.

The Visio files referenced by Top Level SOA and Consumer Website were absent from
the download. Unusable links have been replaced with a note, while the available
raster diagrams are preserved. Other attachments actually used by the document
have been renamed without `pageId`, query strings or problematic characters;
identical images are deduplicated by content.

Internal links and fragments have been repaired. Original section identifiers
are preserved where available. The public addresses of old Confluence pages are
not retained as local redirects: the project uses the new directory tree.

Five source links labeled as order tracking but pointing to the purchase order
service have also been corrected to target `OpcOrderTrackingService`.

`content/migration.json` records original IDs, new paths, attachments and fragment
repairs. Before removal, a complete backup of the download was created at
`/private/tmp/adventure-builder-original-20261119.tar.gz`, outside the site.
The temporary directory is not permanent archival storage.

## Language

All navigation, page descriptions, search messages, accessibility labels,
introductory guides and project documentation are in English, matching the
original technical content. HTML language attributes declare English throughout.

## Verification

`scripts/validate_site.py` checks all declared pages: local destinations, fragments,
duplicate IDs, image alternative text, absence of removed branches and external
runtime dependencies. JavaScript syntax is also checked with
`node --check assets/js/site.js`.

Manual browser checks during the initial reorganization covered the homepage,
technical content search, navigation and diagram display. External bibliographic
links have not been checked for current availability.
