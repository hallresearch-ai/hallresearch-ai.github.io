# Option 2: Research Catalog

This design opens directly onto the Library’s topics. The homepage lists all eleven topic sections in the two broad resource branches, followed by previews of the six forthcoming Research Guides. Topic counts are generated from the same source sections used to build the collection pages. They count source link occurrences, not unique documents or a claim of completeness.

## Visual direction

A white masthead carries the official horizontal Hall Research wordmark above a restrained blue-to-cyan rule. The supplied identity colors—blue `#2D6EBF`, cyan `#059BC0`, graphite `#5E5E5E`, and supporting gray `#848484`—shape links, navigation states, rules, and notices. Self-hosted Montserrat is reserved for headings and interface accents, while long-form source text retains a system sans serif for readability. Square corners and thin rules preserve the research-catalog character. The navigation rail separates the three collections from Library information and becomes an expandable menu on smaller screens.

Collection pages retain their section navigation and source text, but use an open reference-directory layout. The reading area has no enclosing card. Research Guide previews state that they are coming soon and not yet available; no individual guide pages are published.

The homepage’s short topic descriptions and abbreviated provisional guide labels are website navigation additions. They do not replace the underlying source text. The complete “How to Use the Library” source section remains accessible in an expandable panel.

## Preview and maintenance

Run `python3 scripts/preview.py` from this directory and open <http://127.0.0.1:8000/>. The deployable site is in `public/` and includes working browser search.

Edit `assets/css/styles.css` for the visual system and `scripts/build.py` for generated page layouts. Edit `assets/js/site.js` for menu behavior. Rebuild before publishing. Search matching and the commit-pinned source snapshots are retained from the supplied package. No source refresh was requested; the source check date remains October 5, 2026 (UTC).

Locally served logo and font assets keep the design independent of third-party font and image requests. The website has no analytics, advertising, or remote UI dependencies.
