# HallResearch.ai Library website — Option 2: Research Catalog

This is a separate design option based on the supplied website package. The original design remains in the supplied ZIP. This package is a static public interface to the HallResearch.ai Library. It preserves three main Library branches: **AI Governance and Policy Resources**, **AI Assessment and Implementation Resources**, and **AI Research Guides**. Supporting repositories have their own area for examples, prototypes, documentation, teaching materials, and reference tools.

The complete deployable website is already built in `public/`. It has 46 pages, six guide catalog summaries, ten supporting project pages, and a browser search index. See `VERIFICATION_REPORT.md` for this design’s QA results and `DESIGN_NOTES.md` for its visual direction. The original repair report is retained as `BASELINE_VERIFICATION_REPORT.md`; its evidence lives in `baseline-verification/`.

## Preview the built website

Open `DESIGN_PREVIEW.html` for a self-contained visual review. Its controls show desktop and mobile screenshots of the homepage, a resource directory, the guide catalog, and search. To interact with the actual website, start the server below.

From this package directory:

```bash
python3 scripts/preview.py
```

Open <http://127.0.0.1:8000/>. Search requires HTTP; opening the files with `file://` prevents its JSON index from loading. The preview server also returns the site's custom 404 page for missing URLs.

## Deploy with GitHub Pages

1. Copy the contents of this package directory into the root of the intended GitHub repository, including `.github/workflows/pages.yml`.
2. In **Settings → Pages**, choose **GitHub Actions** as the publishing source.
3. Push to `main`, or run the deployment workflow manually.

The workflow installs the small build dependencies, regenerates the site from reviewed source snapshots, validates the output, uploads only `public/`, and deploys it to the `github-pages` environment. Source snapshots, scripts, reports, and build dependencies are excluded from the hosted artifact.

Organization Pages and repository project Pages are supported. Ordinary links are relative to their page. The workflow obtains the actual deployment URL from GitHub Pages and supplies it as `SITE_URL`, including any repository subpath. That value generates canonical and Open Graph URLs, a sitemap, and the base for 404 navigation.

No custom domain is assumed. To use one, configure the real domain and HTTPS in GitHub Pages settings. The workflow will then use that configured URL. For deployment outside this workflow, set `site_url` in `site-config.json`, or supply `SITE_URL` when building. Include a project subpath when applicable. The shipped domain-neutral build omits canonical URLs and the sitemap until the deployment URL is known.

## Rebuild without changing content

Use Node.js 20 or newer and Python 3.12 or newer. Dependencies are version-pinned in `package-lock.json` and `requirements-build.txt`.

```bash
npm ci --omit=dev --ignore-scripts
python3 -m pip install -r requirements-build.txt
python3 scripts/build.py
python3 scripts/audit.py
python3 scripts/check_fidelity.py
```

The build runs without network access. It verifies snapshot hashes against `content/source-manifest.json`. Do not edit generated HTML or the search index directly; a rebuild replaces them.

## Update from the authoritative repositories

```bash
python3 scripts/update_sources.py
python3 scripts/build.py
python3 scripts/audit.py
python3 scripts/check_fidelity.py
```

The updater inventories the public organization, obtains current commit IDs and complete repository trees, and downloads the authoritative Markdown and license files. It also inspects notebook source and bibliography metadata. Refreshes are staged before replacing the snapshots. Review the source changes before committing and publishing them; the deploy workflow intentionally uses the reviewed snapshots rather than fetching editorial changes during deployment.

The three broad source locations are:

- <https://github.com/hallresearch-ai/ai_governance_policy_resources>
- <https://github.com/hallresearch-ai/ai_assessment_implementation_resources>
- <https://github.com/hallresearch-ai/ai_research_guides>

The organization overview comes from `.github/profile/README.md`. Supporting repository documentation remains authoritative in each project repository. `content/source-manifest.json` records the complete repository inventory, source commits, file hashes, and retrieval date.

## What is generated and what is maintained by hand

| Location | Role |
|---|---|
| `public/` | Generated HTML, CSS, JavaScript, favicon, search index, robots file, and deployment metadata |
| `content/upstream/` | Current commit-pinned source documents, licenses, repository trees, and inspection records |
| `content/source-manifest.json` | Snapshot provenance and integrity hashes; written by the updater |
| `content/projects.json` | Short, source-grounded project orientation, audience, and artifact labels |
| `content/document-map.json` | Generated mapping from source Markdown to public pages |
| `scripts/build.py` | Page layout, source transformation, cross-link routing, guide catalog summaries, and indexing |
| `scripts/render-markdown.mjs` | GitHub-flavored Markdown conversion using Marked |
| `assets/` | Website styles, behavior, and favicon; copied into the public output |
| `site-config.json` | Deployment URL configuration and website metadata |
| `verification/` | Current design QA evidence, screenshots, and check results; never deployed |
| `baseline-verification/` | Historical evidence from the supplied design; never deployed |

Resource lists are generated from upstream Markdown. Thousands of links do not need a second manual copy. New H2 sections in the broad collections become pages automatically. A new supporting repository requires an entry in `content/projects.json` and the updater's repository list. A changed guide catalog requires an editorial review of its status and access language; the current landing pages faithfully describe the six guides still under construction. The build refuses an unexpected guide count rather than silently assigning the wrong page routes.

## Repeat the QA checks

```bash
python3 scripts/audit.py
python3 scripts/check_fidelity.py
python3 scripts/check_external.py --sample 280
```

`audit.py` checks every internal page, fragment, asset, and search destination, parses HTML5/JSON/SVG, checks heading order and duplicate IDs, and validates Pages workflow structure. `check_fidelity.py` independently compares source text blocks, exact code blocks, and external URLs with the published documents. Presentation-only badges and their leftover delimiters are excluded from the text comparison.

For browser and accessibility checks:

```bash
npm ci --ignore-scripts
npx playwright install chromium
node scripts/browser-qa.mjs
```

The browser check starts its own preview server. It checks all pages on desktop, representative pages at laptop/tablet/mobile widths, axe accessibility rules, representative searches, keyboard navigation, no-JavaScript navigation, error recovery, and deep-URL 404 behavior. Set `BROWSER_EXECUTABLE` when using an existing compatible Chromium executable.

To test a repository subpath, build to a temporary output directory with a test `SITE_URL`, then set `QA_DIRECTORY` and `QA_BASE_PATH` for the browser check. The domain in such a test is a fixture, not a production setting.

`external-url-inventory.csv` inventories every public external URL. `external-urls-broken-or-uncertain.csv` includes HTTP errors, access challenges, network failures, and links outside the HTTP sample. `not_checked` means exactly that; it does not mean a link is broken. Original upstream URLs remain preserved.

## Attribution and licensing

Patrick Hall and Daniel Atherton maintain the Library, with maintenance and curation sponsored by HallResearch.ai. Source citation examples and editorial AI-assistance disclosures are preserved on the public site. Website adaptations are described on its Methodology page.

Source licenses remain attached to their individual repositories and are included with their snapshots. The model-testing/red-teaming project has separate code and material licenses; both are retained. No single new license is asserted over the collected third-party resources. See `LICENSES.md` for the source license inventory.
