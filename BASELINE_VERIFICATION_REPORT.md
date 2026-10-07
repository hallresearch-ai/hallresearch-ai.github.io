> Historical report from the supplied design. Its `verification/` references now refer to `baseline-verification/`. See `VERIFICATION_REPORT.md` for the alternate design’s current checks.

# Verification and repair report

Verified against the live public HallResearch.ai organization on October 5, 2026 (UTC; October 4 in US Eastern time). The replacement contains 46 generated pages. GitHub remains the editorial source of truth.

## What was checked

All 14 public repositories were inventoried: the 11 required Library/project repositories, the organization profile repository, `basic-chatbot-guidance`, and archived `tabred`. README and supplementary Markdown, repository trees, licenses, notebook source, and bibliography metadata were inspected at recorded commit IDs. The four original large Markdown snapshots matched the current upstream text.

| Check | Result |
|---|---|
| Independent content fidelity | 22 source documents; 4,119 text blocks, 45 exact code blocks, and 2,484 external link occurrences compared; no omissions |
| HTML and internal destinations | All 46 HTML documents parsed; 6,198 internal URL/asset/search-location checks, including 5,124 anchor checks; no errors or duplicate IDs |
| Global search | 2,414 entries; all eight requested representative queries returned relevant results and working page/anchor destinations |
| Browser and responsive layout | All pages at 1440px; nine representative pages also at 1280, 768, 375, and 320px; 82 layout inspections, no page overflow or JavaScript errors |
| Accessibility | 55 axe runs against WCAG A/AA rule sets through 2.2; no automated violations after repair; keyboard, skip-link, menu, error-retry, and no-JavaScript checks passed |
| Project subdirectory | Separate build and HTTP/browser tests under `/library-check/` passed, including search, relative assets, and a deep-URL custom 404 |
| Deployment and metadata | Current official action releases and schemas checked; reviewed-source build and validation precede deployment; only `public/` is uploaded; real Pages URL supplies canonical/OG/sitemap and 404 base |
| External destinations | 2,494 unique URLs inventoried; 245 sampled by HTTP and 106 additional repository file paths verified against live pinned trees |

## Important repairs

- Replaced invented final guide titles with the actual public placeholders, retained reported corpus sizes, and distinguished catalog summaries from released guide assets. The repository currently publishes a catalog README; individual manifests, notebooks, review dates, and changelogs are still pending.
- Restored complete supporting-project READMEs and supplementary documents, setup instructions, background readings, direct notebook/file links, and separate code/material licenses. Added chatbot guidance and a clearly labelled archived TabReD project.
- Preserved the three-branch hierarchy and kept supporting repositories in their companion area. Restored the full Library overview, credits, sponsorship, citations, contribution documents, and editorial AI disclosure.
- Added source-driven regeneration with pinned provenance and hash checks. Replaced the previous audit-only helper and the nonexistent “build script” described by the old Methodology page.
- Rebuilt search with relevant matching, duplicate suppression, area/archive filters, readable snippets, local resource anchors, original-source links, pagination, and a working load-error/retry state. Search and all normal site paths now work under repository subpaths.
- Corrected the source contents link for AI Literacy and K–12 Curricula and the case-mismatched Code of Conduct paths. Added complete section anchors, previous/next navigation, reachable footer/citation/methodology links, and safe 404 recovery.
- Repaired semantic headings, focus states, menu ARIA, labels, horizontal keyboard access to code blocks/tables, responsive side navigation, and code contrast. Removed presentation-only empty GitHub badge delimiters while preserving editorial wording.

## Remaining limitations and editorial decisions

The external HTTP sample returned 195 reachable responses, 7 repeated 404s, and 43 uncertain responses (HTTP restrictions, network errors, or browser challenges). Another 2,143 URLs were outside the HTTP sample. One uncertain URL returned 404 initially but timed out on recheck. See `external-url-inventory.csv` and `external-urls-broken-or-uncertain.csv`; `not_checked` is explicitly distinguished from a broken link. Original source URLs have been preserved. External fragments and the substantive claims of every linked resource were not independently validated.

Maintainers need to finalize the two placeholder guide titles and publish the planned assets. Archived TabReD source documents retain an `arxiv.org/TODO` link and four empty citation links; the empty links are displayed as unavailable text. Its Maps Routing/Weather dataset labels appear crossed with the linked dataset URLs. These source questions are recorded for editorial review, with no replacement resource invented.

The organization profile, Research Guides, and chatbot-guidance trees have no identified repository-wide license file. Source notices remain intact; maintainers can choose the new website code's distribution license separately.

Automated accessibility results and manual layout/contrast/keyboard review support practical AA usability; this is not a formal accessibility certification. Project notebooks and API-dependent examples were inspected, not executed. The actual GitHub Actions run and publication require the target repository's Pages configuration; no live deployment was performed.

The build ships without a production domain. GitHub's workflow supplies it at deployment, so the domain-neutral preview deliberately omits canonical URLs and the sitemap. Maintenance instructions are in `README.md`; detailed evidence is in `verification/`.

A clean rebuild using the declared npm build dependency reproduced every tested public file byte for byte. The final packaged-site link/asset check and ZIP CRC, path-safety, and required-entry checks passed.
