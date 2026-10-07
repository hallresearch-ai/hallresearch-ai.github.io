# Option 2: Research Catalog

This alternate design opens directly onto the Library’s topics. The homepage lists all eleven topic sections in the two broad resource branches, followed by the six Research Guide summaries and a separate introduction to supporting projects. Topic counts are generated from the same source sections used to build the collection pages. They count source link occurrences, not unique documents or a claim of completeness.

## Visual direction

A dark ink masthead, warm white reading surface, and vivid blue links give the Library a clear typographic identity. Sans-serif headings, square corners, and thin rules carry through every page. The left navigation rail separates the main branches from supporting projects and Library information. The rail becomes an expandable menu on smaller screens.

Collection pages retain their section navigation and source text, but use an open reference-directory layout. The reading area has no enclosing card. Research Guide previews display development status, including the two pending titles; full source placeholders remain visible in the authoritative catalog and guide pages.

The homepage’s short topic descriptions and abbreviated provisional guide labels are website navigation additions. They do not replace the underlying source text. The complete “How to Use the Library” source section remains accessible in an expandable panel.

## Preview and maintenance

Run `python3 scripts/preview.py` from this directory and open <http://127.0.0.1:8000/>. The deployable site is in `public/`. This package includes the full 46-page site and working browser search, not just a homepage drawing. No publication or deployment has been performed.

Edit `assets/css/styles.css` for the visual system and `scripts/build.py` for generated page layouts. Edit `assets/js/site.js` for menu behavior. Rebuild before publishing. Search matching and the commit-pinned source snapshots are retained from the supplied package. No source refresh was requested; the source check date remains October 5, 2026 (UTC).

System fonts and locally served assets keep the design independent of third-party font and image requests. The website has no analytics, advertising, or remote UI dependencies.
