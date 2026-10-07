# Option 2 verification report

Design prepared October 7, 2026. This is a separate Research Catalog design based on the supplied HallResearch.ai Library website ZIP. The source snapshots were retained without a refresh; their recorded check date is October 5, 2026 (UTC).

## What changed

The homepage now exposes all eleven topic sections across the two broad collections, followed by six Research Guide previews and a distinct supporting-project area. A dark masthead, blue accent, sans-serif headings, and open ruled rows replace the earlier reading-room presentation. All 46 pages use the new layout. Main navigation sits in a desktop rail and opens through an accessible Browse button on smaller screens. Source tables retain their horizontal scrolling regions and have larger link targets.

Topic counts are generated from source link occurrences. Provisional guide labels are abbreviated only on homepage previews, with their pending title and construction status explicitly shown; full placeholders remain in the source catalog and guide pages. Supporting projects remain separate from the three main branches.

## Current checks

- Internal audit: 46 HTML5 documents, 6,309 internal references, 5,124 anchor references, and 2,414 search entries checked, with no errors.
- Independent content comparison: all 22 source documents represented, covering 4,119 text blocks, 45 exact code blocks, and 2,484 external link occurrences. No missing source text, code, or external links.
- Browser layout: 82 checks, including every page at 1440px and nine representative pages at 1280, 768, 375, and 320px. No horizontal page overflow or JavaScript errors.
- Automated accessibility: 55 axe runs covering WCAG A/AA rules through 2.2, with zero reported violations after enlarging adjacent links in a technical resource table. This is automated testing, not a formal accessibility certification.
- Search: prompt injection, red teaming, AI incidents, labor, NIST AI RMF, explainability, university policy, and system card queries return results. Resource navigation, area filtering, pagination, empty results, fetch failure/retry, keyboard skip navigation, mobile menu state and Escape focus, reduced motion, deep-URL 404 navigation, and no-JavaScript fallbacks passed.
- Visual review: rendered homepage layouts were inspected at desktop and mobile sizes. Eight additional screenshots capture the homepage, an incident resource directory, guide catalog, and search at both sizes, with no overflow. The self-contained `DESIGN_PREVIEW.html` uses these exact screenshots. Its eight view/device combinations and four responsive widths were checked, with no preview script errors, overflow, or automated accessibility violations.

The complete current evidence is in `verification/`. Historical QA and outward-link inventories from the supplied package are retained separately in `baseline-verification/`, `BASELINE_VERIFICATION_REPORT.md`, and the root CSV inventories. Outward URLs were not rechecked during this design pass. Unfinished guide material and known source URL problems remain documented in that baseline report.

## Preview and publication

The standalone design preview works without a server. For the actual site and working search, run `python3 scripts/preview.py` and open <http://127.0.0.1:8000/>. Build dependencies, source snapshots, update scripts, and the GitHub Pages workflow are included. The archive excludes installed dependencies and browser binaries. No website has been published or deployed during this design pass.
