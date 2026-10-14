#!/usr/bin/env python3
"""Build the static Library from pinned upstream Markdown, without network access."""
from collections import Counter
from copy import deepcopy
import hashlib
import html as escape_html
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import unicodedata
from urllib.parse import quote, unquote, urlsplit
from lxml import etree, html

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'content/upstream'
OUT = Path(os.environ.get('OUTPUT_DIR', ROOT / 'public')).resolve()
CONFIG = json.loads((ROOT / 'site-config.json').read_text())
SITE_URL = (os.environ.get('SITE_URL') or CONFIG.get('site_url', '')).rstrip('/')
MANIFEST = json.loads((ROOT / 'content/source-manifest.json').read_text())
CHECKED = MANIFEST['checked_at_utc'][:10]
BRANCHES = {
    'ai_governance_policy_resources': ('governance', 'AI Governance and Policy Resources', 'AI governance, public policy, law, institutional guidance, incidents, accountability, labor, and social impact.'),
    'ai_assessment_implementation_resources': ('assessment', 'AI Assessment and Implementation Resources', 'Responsible machine learning assessment, implementation, evaluation, auditing, testing, tooling, documentation, and education.')}
GUIDE_SLUGS = ['governing-ai-agents', 'adversarial-testing', 'evidence-ai-performance', 'learning-from-ai-failures', 'ai-risk-management', 'ai-and-labor']
DOCUMENTS, DOC_URLS, HEADING_URLS, PAGES, NOTES = {}, {}, {}, {}, []
REPOS = {p.name: json.loads((p / 'repository.json').read_text()) for p in UPSTREAM.iterdir() if p.is_dir()}
TREES = {name: {x['path']: x for x in json.loads((UPSTREAM / name / 'tree.json').read_text())['tree']} for name in REPOS}

def esc(s):
    return escape_html.escape(str(s), quote=True)

def text(node):
    return re.sub(r'\s+', ' ', node.text_content()).strip()

def clean_title(s):
    return re.sub(r'^[^\w]+', '', s).strip()

def slug(s):
    # GitHub heading slugs preserve a leading hyphen after an emoji + space.
    s = s.lower().replace(' ', '-')
    return ''.join(c for c in s if c in '-_' or unicodedata.category(c)[0] in 'LN')

def serial(node):
    return html.tostring(node, encoding='unicode', method='html')

def contents(node):
    return (node.text or '') + ''.join(serial(c) for c in node)

def fragment(raw):
    return html.fragment_fromstring(raw, create_parent='div')

def strip_presentation(md):
    # The original centered wrapper is GitHub presentation, not prose.
    md = re.sub(r'<div\s+align=["\']center["\']\s*>', '', md)
    md = md.replace('</div>', '') if '<div' not in md else md
    return md

def init_sources():
    sources = {}
    for item in MANIFEST['repositories']:
        name = item['repo']
        for file in item['files']:
            path = file['path']
            if hashlib.sha256((UPSTREAM / name / path).read_bytes()).hexdigest() != file['sha256']:
                raise RuntimeError(f'Source snapshot hash differs from its manifest: {name}/{path}')
            if path.lower().endswith('.md'):
                key = name + '/' + path
                sources[key] = strip_presentation((UPSTREAM / key).read_text())
                if name in BRANCHES and path.lower() == 'readme.md':
                    DOC_URLS[key] = BRANCHES[name][0] + '/index.html'
                elif name == '.github' and path == 'profile/README.md':
                    DOC_URLS[key] = 'library-overview.html'
                elif name == 'ai_research_guides' and path.lower() == 'readme.md':
                    DOC_URLS[key] = 'guides/index.html'
                else:
                    area = BRANCHES[name][0] if name in BRANCHES else 'guides/materials'
                    DOC_URLS[key] = area + '/' + slug(str(Path(path).with_suffix('')).replace('/', '-')) + '.html'
    result = subprocess.run(['node', str(ROOT / 'scripts/render-markdown.mjs')], input=json.dumps(sources), text=True, capture_output=True, check=True)
    raw = json.loads(result.stdout)
    for key, rendered in raw.items():
        doc = fragment(rendered)
        seen = Counter()
        for h in doc.xpath('.//h1|.//h2|.//h3|.//h4|.//h5|.//h6'):
            ident = slug(text(h)) or 'section'
            seen[ident] += 1
            h.set('id', ident if seen[ident] == 1 else ident + '-' + str(seen[ident] - 1))
            HEADING_URLS[(key, h.get('id'))] = DOC_URLS[key] + '#' + h.get('id')
        for img in doc.xpath('.//img'):
            if 'img.shields.io/' in img.get('src', ''):
                label = img.get('alt', '')
                replacement = html.Element('span', {'class': 'badge'})
                replacement.text = label
                replacement.tail = img.tail
                img.getparent().replace(img, replacement)
            else:
                img.set('loading', 'lazy')
                img.set('alt', img.get('alt', ''))
        for badge in list(doc.xpath('.//span[@class="badge"]')):
            if not badge.text:
                previous = badge.getprevious()
                if previous is not None and previous.tail:
                    previous.tail = re.sub(r'\s*\|\s*$', '', previous.tail)
                if badge.tail:
                    if previous is not None: previous.tail = (previous.tail or '') + badge.tail
                    else: badge.getparent().text = (badge.getparent().text or '') + badge.tail
                badge.getparent().remove(badge)
        for checkbox in doc.xpath('.//input[@type="checkbox"]'):
            span = html.Element('span', {'class': 'task-status', 'role': 'img', 'aria-label': 'Completed' if 'checked' in checkbox.attrib else 'Planned'})
            span.text = '☑' if 'checked' in checkbox.attrib else '☐'
            span.tail = checkbox.tail
            checkbox.getparent().replace(checkbox, span)
        for p in doc.xpath('.//blockquote/p[1]'):
            if p.text and re.match(r'^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', p.text):
                kind = re.match(r'^\[!(\w+)\]', p.text).group(1)
                p.text = re.sub(r'^\[!\w+\]', kind.title() + '.', p.text, count=1)
                p.getparent().set('class', 'source-note')
        for a in list(doc.xpath('.//a')):
            if not a.get('href') and not a.get('id'):
                a.tag = 'span'; a.attrib.clear(); a.set('class', 'unavailable-link')
                a.set('title', 'The upstream document does not supply this link.')
                NOTES.append({'source': key, 'kind': 'empty upstream link', 'label': text(a)})
            elif not text(a) and not a.xpath('.//img'):
                parent = a.getparent()
                if a.tail:
                    previous = a.getprevious()
                    if previous is None: parent.text = (parent.text or '') + a.tail
                    else: previous.tail = (previous.tail or '') + a.tail
                parent.remove(a)
        DOCUMENTS[key] = doc

def parts(doc):
    sections, intro, current = [], [], None
    for node in doc:
        if node.tag == 'h2':
            current = {'title': text(node), 'id': node.get('id'), 'nodes': []}
            sections.append(current)
        if current is None: intro.append(node)
        else: current['nodes'].append(node)
    return intro, sections

def register_branch_urls():
    for name, (area, _, _) in BRANCHES.items():
        key = name + '/README.md'
        for section in parts(DOCUMENTS[key])[1]:
            if section['title'] == 'Contents': continue
            page = area + '/' + slug(clean_title(section['title'])) + '.html'
            section['page'] = page
            for node in section['nodes']:
                for h in [node] + list(node.iterdescendants()):
                    if h.tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
                        HEADING_URLS[(key, h.get('id'))] = page + '#' + h.get('id')

def source_url(repo, path, image=False):
    sha = REPOS[repo]['commit']
    if image:
        return f'https://raw.githubusercontent.com/hallresearch-ai/{repo}/{sha}/' + quote(path, safe='/')
    kind = 'tree' if TREES[repo].get(path, {}).get('type') == 'tree' else 'blob'
    return f'https://github.com/hallresearch-ai/{repo}/{kind}/{sha}/' + quote(path, safe='/')

def resolve_link(value, key, image=False, local=True):
    repo, path = key.split('/', 1)
    u = urlsplit(value)
    if not u.scheme and not u.netloc:
        if not u.path:
            anchor = unquote(u.fragment)
            if anchor and (key, anchor) not in HEADING_URLS:
                matches = [ident for source, ident in HEADING_URLS if source == key and ident.replace('-', '') == anchor.replace('-', '')]
                if len(matches) == 1:
                    NOTES.append({'source': key, 'kind': 'corrected upstream contents anchor', 'original': value, 'resolved': matches[0]})
                    anchor = matches[0]
            return HEADING_URLS.get((key, anchor), DOC_URLS[key] + ('#' + anchor if anchor else ''))
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(u.path)))
        if target not in TREES[repo]:
            same = [p for p in TREES[repo] if p.lower() == target.lower()]
            if len(same) == 1:
                NOTES.append({'source': key, 'kind': 'case-corrected repository path', 'original': value, 'resolved': same[0]})
                target = same[0]
            else:
                NOTES.append({'source': key, 'kind': 'unresolved repository path', 'original': value})
        doc_key = repo + '/' + target
        if local and doc_key in DOC_URLS and not image:
            return HEADING_URLS.get((doc_key, unquote(u.fragment)), DOC_URLS[doc_key] + ('#' + u.fragment if u.fragment else ''))
        return source_url(repo, target, image) + ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')
    if u.scheme == '' and u.netloc: return 'https:' + value
    if local and not image and u.netloc == 'github.com':
        match = re.fullmatch(r'/hallresearch-ai(?:/([^/]+))?/?', u.path)
        if match:
            target_repo = match.group(1) or '.github'
            readme = next((k for k in DOC_URLS if k.startswith(target_repo + '/') and Path(k).name.lower() == 'readme.md'), None)
            if readme:
                return HEADING_URLS.get((readme, unquote(u.fragment)), DOC_URLS[readme] + ('#' + u.fragment if u.fragment else ''))
    return value

def source_fragment(nodes, key, base_level=2, remove_title=False, citations=False):
    wrapper = html.Element('div', {'class': 'source-content', 'data-source-document': key})
    for node in nodes: wrapper.append(deepcopy(node))
    if remove_title:
        first = next((n for n in wrapper if n.tag in ('h1', 'h2')), None)
        if first is not None: wrapper.remove(first)
    heading_nodes = wrapper.xpath('.//h1|.//h2|.//h3|.//h4|.//h5|.//h6')
    if heading_nodes:
        minimum = min(int(n.tag[1]) for n in heading_nodes)
        first_level = int(heading_nodes[0].tag[1])
        for node in heading_nodes:
            level = int(node.tag[1])
            # Some prompt documents begin with H4s before later H2s. Their
            # section text stays intact while the presentation has a valid outline.
            node.tag = 'h' + str(min(6, max(base_level, level - max(minimum, first_level) + base_level)))
    in_citations = citations
    for top in wrapper:
        if top.tag.startswith('h') and text(top) == 'Suggested Citation': in_citations = True
        for a in top.xpath('descendant-or-self::a[@href]'):
            if a.get('data-site-link'):
                del a.attrib['data-site-link']
            else:
                a.set('href', resolve_link(a.get('href'), key, local=not in_citations))
        for img in top.xpath('descendant-or-self::img[@src]'):
            img.set('src', resolve_link(img.get('src'), key, image=True))
    for table in list(wrapper.xpath('.//table')):
        region = html.Element('div', {'class': 'table-wrap', 'tabindex': '0', 'role': 'region', 'aria-label': 'Scrollable source table'})
        table.getparent().replace(table, region)
        region.append(table)
        for th in table.xpath('.//thead//th'): th.set('scope', 'col')
    for pre in wrapper.xpath('.//pre'):
        pre.set('tabindex', '0')
    return serial(wrapper)

def provenance(key):
    repo, path = key.split('/', 1)
    license_info = REPOS[repo].get('license')
    license_label = license_info.get('spdx_id') if license_info else 'No repository-wide license identified'
    return f'<div class="provenance"><p><a href="{esc(source_url(repo, path))}">View the source document on GitHub</a> · Sources checked {CHECKED} (UTC).</p><p>{esc(license_label)}. Source text is preserved; navigation and formatting are adapted for this website.</p></div>'

def add_page(path, title, description, body, area='', breadcrumbs=None, noindex=False):
    PAGES[path] = dict(title=title, description=description, body=body, area=area, breadcrumbs=breadcrumbs or [], noindex=noindex)

def head(title, lede='', eyebrow='', crumbs=None, ident=None):
    trail = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Library</a></li>'
    for label, url in (crumbs or []):
        trail += '<li>' + (f'<a href="{esc(url)}">{esc(label)}</a>' if url else f'<span aria-current="page">{esc(label)}</span>') + '</li>'
    trail += '</ol></nav>'
    return f'<section class="page-head">{trail}<p class="eyebrow">{esc(eyebrow)}</p><h1' + (f' id="{esc(ident)}"' if ident else '') + f'>{esc(title)}</h1>' + (f'<p class="lede">{esc(lede)}</p>' if lede else '') + '</section>'

def sidebar(label, links, on_page=None):
    body = f'<aside class="sidebar" aria-label="{esc(label)}"><details class="section-nav" open><summary>{esc(label)}</summary><nav aria-label="{esc(label)} sections">'
    for title, url, active in links:
        body += f'<a href="{esc(url)}"' + (' aria-current="page" class="current"' if active else '') + f'>{esc(title)}</a>'
    body += '</nav></details>'
    if on_page:
        body += '<details class="local-toc" open><summary>On this page</summary><nav aria-label="On this page">'
        for title, ident, level in on_page:
            body += f'<a class="level-{level}" href="#{esc(ident)}">{esc(title)}</a>'
        body += '</nav></details>'
    return body + '</aside>'

def about_sidebar(current):
    return sidebar('About the Library', [(t, p, p == current) for t,p in [('About', 'about.html'), ('Library overview', 'library-overview.html'), ('Methodology', 'methodology.html'), ('How to cite', 'cite.html')]])

def build_branches():
    for repo, (area, title, description) in BRANCHES.items():
        key = repo + '/README.md'; intro, all_sections = parts(DOCUMENTS[key])
        sections = [s for s in all_sections if s['title'] != 'Contents']
        page_links = [(clean_title(s['title']), area + '/' + slug(clean_title(s['title'])) + '.html') for s in sections]
        body = head(title, description, 'Main Library branch', [(title, None)])
        body += '<section class="wrap"><article class="prose branch-intro">' + source_fragment(intro, key, remove_title=True) + '</article><h2>Browse this branch</h2><div class="section-index">'
        for s, (st, url) in zip(sections, page_links):
            links = sum(len(n.xpath('.//a[@href]')) for n in s['nodes'])
            archived = 'Archived material · ' if 'Archived' in st else ''
            body += f'<a class="section-item" href="{url}"><h3>{esc(st)}</h3><span class="meta">{archived}{links:,} source links</span><span aria-hidden="true"> →</span></a>'
        body += '</div><details class="full-index"><summary>Full contents</summary>'
        toc = next(s for s in all_sections if s['title'] == 'Contents')
        body += source_fragment(toc['nodes'], key) + '</details>' + provenance(key) + '</section>'
        add_page(area + '/index.html', title, description, body, area)
        for i, (s, (st, url)) in enumerate(zip(sections, page_links)):
            raw = source_fragment(s['nodes'], key, remove_title=True)
            doc = fragment(raw)
            headings = [(text(h), h.get('id'), int(h.tag[1])) for h in doc.xpath('.//h2|.//h3')]
            if area == 'governance' and len(headings) > 70:
                headings = [h for h in headings if h[2] == 2]
            nav = sidebar(title, [('Branch overview', area + '/index.html', False)] + [(a,b,b==url) for a,b in page_links], headings)
            body = head(st, '', 'Archived collection' if 'Archived' in st else title, [(title, area + '/index.html'), (st,None)], s['id'])
            body += '<div class="content-layout">' + nav + '<article class="prose">'
            if 'Archived' in st:
                body += '<p class="notice">This section contains material classified as archived in the source repository. Consult the source notes for publication and archive dates.</p>'
            body += raw + provenance(key) + '<nav class="pagination" aria-label="Adjacent sections">'
            if i: body += f'<a href="{page_links[i-1][1]}">← {esc(page_links[i-1][0])}</a>'
            if i+1<len(page_links): body += f'<a href="{page_links[i+1][1]}">{esc(page_links[i+1][0])} →</a>'
            body += '</nav></article></div>'
            add_page(url, st, f'{st}. Curated resources from the {title} branch of the HallResearch.ai Library.', body, area)

def guide_rows():
    table = DOCUMENTS['ai_research_guides/README.md'].xpath('.//table')[0]
    rows = []
    for tr in table.xpath('.//tbody/tr'):
        cells = tr.findall('td')
        rows.append({'title': text(cells[1]), 'count': text(cells[2]), 'description': text(cells[3])})
    if len(rows) != len(GUIDE_SLUGS):
        raise RuntimeError('Research-guide catalog changed; review the routing before building.')
    return rows

def build_guides():
    key = 'ai_research_guides/README.md'; rows = guide_rows()
    doc = deepcopy(DOCUMENTS[key])
    doc.xpath('.//table')[0].xpath('.//thead/tr/th')[0].text = 'Topic'
    # The GitHub tagline is a subtitle, not a heading below the site title.
    for h in doc.xpath('.//h3'):
        if text(h) == 'Curated pathways through the HallResearch.ai Library': h.tag='p'; h.set('class','source-subtitle')
    body = head('AI Research Guides', 'Focused research pathways are in development and not yet available.', 'Coming soon', [('AI Research Guides',None)])
    body += '<div class="content-layout">' + sidebar('Research Guides', [('Guide catalog', 'guides/index.html', True)])
    body += '<article class="prose"><p class="notice guide-coming-soon"><strong>Coming soon.</strong> The AI Research Guides are under construction and have not yet been released. The catalog below previews the planned initial collection; guide content and public access will be added as each guide is completed.</p>' + source_fragment(list(doc), key, remove_title=True) + provenance(key) + '</article></div>'
    add_page('guides/index.html', 'AI Research Guides — Coming soon', 'Planned topic-focused research guides. Guide content is under construction and not yet available.', body, 'guides')

def build_extra_documents():
    primary={r+'/README.md' for r in BRANCHES}|{'ai_research_guides/README.md','.github/profile/README.md'}
    for key,url in DOC_URLS.items():
        if url in PAGES or key in primary:continue
        repo,path=key.split('/',1); doc=DOCUMENTS[key]
        hs=doc.xpath('.//h1|.//h2'); title=text(hs[0]) if hs else Path(path).stem.replace('-',' ')
        if 'Code-of-Conduct' in path:title='Contributor Code of Conduct'
        area=BRANCHES[repo][0] if repo in BRANCHES else 'guides'
        parent=BRANCHES[repo][1] if repo in BRANCHES else 'AI Research Guides'
        parent_url=area+'/index.html'
        body=head(title,'',parent,[(parent,parent_url),(title,None)])+'<section class="wrap"><article class="prose">'+source_fragment(list(doc),key,remove_title=bool(doc.xpath('./h1')))+provenance(key)+'</article></section>'
        add_page(url,title+' · '+parent,f'{title}: source documentation from {parent}.',body,area)

def build_about():
    key='.github/profile/README.md'; intro,sections=parts(DOCUMENTS[key]); by_title={s['title']:s for s in sections}
    overview=head('HallResearch.ai Library','The complete Library overview, with its philosophy, organization, maintenance notes, and suggested citations.','About the Library',[('About','about.html'),('Library overview',None)])
    overview+='<div class="content-layout">'+about_sidebar('library-overview.html')+'<article class="prose">'+source_fragment(list(DOCUMENTS[key]),key,remove_title=True)+provenance(key)+'</article></div>'
    add_page('library-overview.html','HallResearch.ai Library overview','The authoritative Library overview, including its three collections, philosophy, maintenance, and citations.',overview,'about')
    nodes=[]
    for section_title in ['Library Philosophy','Repository Organization','Legacy Note','Maintenance Note']:nodes.extend(by_title[section_title]['nodes'])
    about=head('A working research library.','A public collection maintained by Patrick Hall and Daniel Atherton, with curation sponsored by HallResearch.ai.','About the Library',[('About',None)])
    about+='<div class="content-layout">'+about_sidebar('about.html')+'<article class="prose">'+source_fragment(nodes,key)+'<h2>Contribute to the Library</h2><p>Suggestions, corrections, and additions are welcome through the relevant repository.</p><ul>'
    for repo,(area,label,_) in BRANCHES.items():
        about+=f'<li><a href="{area}/contributing.html">{esc(label)}: contribution guidelines</a> · <a href="{area}/code-of-conduct.html">Code of Conduct</a> · <a href="https://github.com/hallresearch-ai/{repo}/issues">Report a correction on GitHub</a></li>'
    about+='</ul><p><a href="library-overview.html">Read the complete Library overview</a>.</p>'+provenance(key)+'</article></div>'
    add_page('about.html','About the Library','Library philosophy, organization, credits, sponsorship, maintenance, AI disclosure, and contribution guidance.',about,'about')
    citation=by_title['Suggested Citation']['nodes'][1:]
    body=head('How to cite the Library','Use the main Library citation or the citation for the specific branch you used. Update access dates to match your own use.','Citation guidance',[('About','about.html'),('How to cite',None)])
    body+='<div class="content-layout">'+about_sidebar('cite.html')+'<article class="prose">'+source_fragment(citation,key,citations=True)+provenance(key)+'</article></div>'
    add_page('cite.html','How to cite the Library','Source-preserved MLA, APA, Chicago, ACM, and BibTeX citation examples for the Library and each main branch.',body,'about')
    body=head('How the Library is maintained','The website presents the research collection maintained in HallResearch.ai’s public repositories.','Curation and publishing',[('About','about.html'),('Methodology',None)])
    body+='<div class="content-layout">'+about_sidebar('methodology.html')+'''<article class="prose"><h2>Source of truth</h2><p>The three main GitHub repositories remain authoritative. The website preserves their editorial text and resource links while adding browsing, cross-links, and search.</p><h2>Curation</h2><p>The Library is maintained as an ongoing public resource. Suggestions, corrections, and additions continue through the relevant repository’s issue tracker or pull request process. The Library’s <a href="about.html#maintenance-note">maintenance note</a> includes its AI-assistance disclosure.</p><h2>Publication status</h2><p>Archived collections remain labelled. AI Research Guides are clearly marked as coming soon: their planned catalog is visible, but guide content is not yet available.</p><h2>Search</h2><p>Search covers the Governance and Assessment collections and the Research Guide catalog. Results identify their Library context, link to the matching item on the site, and provide the resource’s original URL. Archived items can be filtered separately.</p><h2>Source freshness</h2>'''+f'<p>Public source files were checked on {CHECKED} (UTC). The website is a snapshot of those files; subsequent repository changes will appear after the next update. See the <a href="library-overview.html">Library overview</a> for scope and maintenance information.</p><h2>Website adaptation</h2><p>This website uses automated tooling to inspect and transform public source files. The source repositories’ own editorial disclosures are preserved; website navigation and orientation text are presentation additions.</p></article></div>'
    add_page('methodology.html','Methodology','The website’s authoritative sources, content preservation, search, publication status, source freshness, and adaptation disclosure.',body,'about')

def build_home():
    key='.github/profile/README.md'; _,sections=parts(DOCUMENTS[key]); how=next(s for s in sections if s['title']=='How to Use the Library')
    summaries={
        'Institutional AI Governance':'University policies and guidance for teaching.',
        'Government and Multilateral AI Policy Guidance':'National, regional, and international frameworks.',
        'Legal and Regulatory Materials':'Legal documents and trackers for AI law and policy.',
        'AI Incidents and Accountability':'Incident databases, reporting systems, and research on AI failures.',
        'AI, Labor, and Social Impact':'Work, civil society, environmental costs, and critical perspectives.',
        'Organizations, Bibliographies, and Resource Lists':'Research communities and routes into related collections.',
        'Archived Governance Materials':'Earlier policy, frameworks, and guidance retained for reference.',
        'Assessment and Implementation Guidance':'Resources for responsible assessment and implementation.',
        'Technical Resources':'Evaluation, testing, auditing, documentation, and tooling.',
        'Education Resources':'Teaching and learning materials for responsible AI practice.',
        'Archived':'Earlier assessment material retained for reference.'}
    body='''<section class="hero"><p class="eyebrow">A public research collection</p><h1>AI governance,<br>policy &amp; practice.</h1><p class="lede">Explore the HallResearch.ai Library, a curated collection for understanding and assessing AI systems in the world.</p><form class="hero-search" action="search.html" method="get" role="search"><label class="sr-only" for="home-query">Search the Library</label><input id="home-query" name="q" type="search" placeholder="Search the collection…" required><button type="submit">Search <span aria-hidden="true">↗</span></button></form><p class="source-date"><span class="source-dot" aria-hidden="true"></span>Public source snapshot · '''+CHECKED+''' (UTC)</p></section><section class="wrap catalog-home" aria-labelledby="catalog-heading"><div class="section-title"><h2 id="catalog-heading">Browse the collections</h2><p>Start with a subject. Follow the sources.</p></div>'''
    for number,(repo,(area,title,description)) in enumerate(BRANCHES.items(),1):
        branch_sections=[s for s in parts(DOCUMENTS[repo+'/README.md'])[1] if s['title']!='Contents']
        body+=f'<section class="catalog-group" aria-labelledby="catalog-{area}"><div class="catalog-group-head"><h3 id="catalog-{area}"><span class="group-number" aria-hidden="true">0{number}</span><a href="{area}/index.html">{esc(title)}</a></h3><a class="group-link" href="{area}/index.html">Branch overview <span aria-hidden="true">↗</span></a></div><div class="catalog-list">'
        for i,s in enumerate(branch_sections,1):
            st=clean_title(s['title']);links=sum(len(n.xpath('.//a[@href]')) for n in s['nodes']);archived='Archived' in st
            description=summaries.get(st,'Browse the resources in this collection.')
            display='Archived Assessment Materials' if st=='Archived' else st
            body+=f'<a class="catalog-row'+(' archived-row' if archived else '')+f'" href="{area}/{slug(st)}.html"><span class="row-number" aria-hidden="true">{number}.{i:02}</span><div class="row-content"><h4>{esc(display)}</h4><span class="row-description">{esc(description)}</span></div><span class="row-count"><strong>{links:,}</strong><span>source links</span></span><span class="row-arrow" aria-hidden="true">↗</span></a>'
        body+='</div></section>'
    body+='''<section class="catalog-group guide-group" aria-labelledby="catalog-guides"><div class="catalog-group-head"><h3 id="catalog-guides"><span class="group-number" aria-hidden="true">03</span><a href="guides/index.html">AI Research Guides — Coming soon</a></h3><a class="group-link" href="guides/index.html">Preview catalog <span aria-hidden="true">↗</span></a></div><p class="notice guide-coming-soon"><strong>Not yet available.</strong> The initial Research Guide collection is under construction. These topics preview what is coming first.</p><div class="guide-preview-list">'''
    for row,route in zip(guide_rows(),GUIDE_SLUGS):
        provisional='[INSERT' in row['title'];display=re.sub(r'\s+(and|&)$','',row['title'].split('[')[0].strip())
        body+=f'<div class="guide-preview"><div class="guide-preview-main"><h4>{esc(display)}</h4><span class="row-description">{esc(row["description"])}</span></div><span class="guide-state">'+('Title pending · ' if provisional else '')+'Coming soon</span></div>'
    body+='</div></section><details class="home-orientation"><summary>How the Library is organized</summary><div>'+source_fragment(how['nodes'],key)+'</div></details></section>'
    add_page('index.html','HallResearch.ai Library',CONFIG['description'],body,'home')

def build_search_and_404():
    body=head('Search the Library','Find resources across Governance, Assessment, and the forthcoming Research Guide catalog.','Search',[('Search',None)])+'''<section class="search-page"><form id="search-form" action="search.html" method="get" role="search"><label for="q">Search terms</label><div class="search-box"><input id="q" name="q" type="search" placeholder="Try prompt injection or university policy"><button type="submit">Search</button></div><div class="search-filters"><label for="area">Library area<select id="area" name="area"><option value="">All areas</option><option value="governance">Governance and Policy</option><option value="assessment">Assessment and Implementation</option><option value="guides">Research Guides — Coming soon</option></select></label><label class="checkbox-label"><input id="include-archived" type="checkbox" checked>Include archived material</label></div></form><p id="search-status" role="status" aria-live="polite">Loading search…</p><div id="results" class="results" role="region" aria-label="Search results"></div><button id="more-results" type="button" hidden>Show more results</button><button id="retry-search" type="button" hidden>Retry loading search</button><noscript><p>Search needs JavaScript. Browse <a href="governance/index.html">Governance</a>, <a href="assessment/index.html">Assessment</a>, or preview the <a href="guides/index.html">forthcoming Research Guides</a>.</p></noscript></section>'''
    add_page('search.html','Search the Library','Search curated AI governance, policy, assessment, implementation, and forthcoming Research Guide resources.',body,'search',noindex=True)
    body=head('Page not found','The requested page could not be found.','404',[('Page not found',None)])+'''<section class="wrap"><p><a class="button" href="index.html">Return to the Library</a></p><p>Browse <a href="governance/index.html">Governance</a>, <a href="assessment/index.html">Assessment</a>, or preview the <a href="guides/index.html">forthcoming Research Guides</a>.</p><form class="hero-search" action="search.html" method="get" role="search"><label class="sr-only" for="missing-query">Search the Library</label><input id="missing-query" type="search" name="q" required><button type="submit">Search</button></form></section>'''
    add_page('404.html','Page not found','The requested Library page could not be found.',body,noindex=True)

def relative_urls(raw,path):
    doc=fragment(raw)
    directory=posixpath.dirname(path) or '.'
    for node in doc.xpath('.//*[@href or @src or @action]'):
        for attr in ('href','src','action'):
            value=node.get(attr)
            if value is None:continue
            u=urlsplit(value)
            if u.scheme or u.netloc or value.startswith('#'):continue
            target=posixpath.relpath(u.path or path,directory)
            node.set(attr,target+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else ''))
    return contents(doc)

def write_pages():
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',ignore=shutil.ignore_patterns('search-index.json'))
    nav_items=[('home','Home','index.html'),('governance','Governance','governance/index.html'),('assessment','Assessment','assessment/index.html'),('guides','Research Guides — Coming soon','guides/index.html'),('about','About','about.html'),('search','Search','search.html')]
    for path,p in PAGES.items():
        nav='<header class="site-header"><div class="nav"><a class="brand" href="index.html"><img class="brand-logo" src="assets/logo.svg" alt="Hall Research"><span class="brand-library">Library</span></a><p class="masthead-note">Curated by Patrick Hall &amp; Daniel Atherton</p><button class="mobile-toggle" type="button" aria-controls="main-navigation" aria-expanded="false" hidden>Browse</button></div></header><div class="catalog-shell"><aside class="catalog-rail"><nav class="nav-links" id="main-navigation" aria-label="Main navigation"><p class="rail-label">The collection</p>'
        rail_numbers={'governance':'01','assessment':'02','guides':'03'}
        for area,title,url in nav_items:
            if area=='about':nav+='<p class="rail-label rail-separator">Using the Library</p>'
            display='All collections' if area=='home' else title
            number=rail_numbers.get(area,'')
            active=p['area']==area and not (area=='about' and path in ('cite.html','methodology.html'))
            nav+=f'<a href="{url}"'+(' aria-current="page" class="active"' if active else '')+f'><span>{display}</span>'+ (f'<span class="rail-number" aria-hidden="true">{number}</span>' if number else '')+'</a>'
        for label,url in [('How to cite','cite.html'),('Methodology','methodology.html')]:
            nav+=f'<a href="{url}"'+(' aria-current="page" class="active"' if path==url else '')+f'>{label}</a>'
        nav+='</nav><div class="rail-foot"><p>A working public collection.</p><a href="https://github.com/hallresearch-ai">Source repositories <span aria-hidden="true">↗</span></a></div></aside><div class="catalog-content">'
        footer='''<footer class="footer"><div class="footer-inner"><div><strong>HallResearch.ai Library</strong><p>Maintained by Patrick Hall and Daniel Atherton.<br>Curation sponsored by <a href="https://hallresearch.ai/">HallResearch.ai</a>.</p></div><nav aria-label="Footer navigation"><a href="about.html">About</a><a href="methodology.html">Methodology</a><a href="cite.html">How to cite</a><a href="https://github.com/hallresearch-ai/.github/blob/main/profile/README.md">GitHub profile edition</a><a href="https://github.com/hallresearch-ai">Source repositories on GitHub</a></nav></div></footer>'''
        full=relative_urls('<a class="skip-link" href="#main-content">Skip to content</a>'+nav+'<main id="main-content" tabindex="-1">'+p['body']+'</main>'+footer+'</div></div>'+('<script type="module" src="assets/js/search.js"></script>' if path=='search.html' else '')+'<script src="assets/js/site.js" defer></script>',path)
        metadata=f'<meta name="description" content="{esc(p["description"])}"><meta property="og:type" content="website"><meta property="og:site_name" content="HallResearch.ai Library"><meta property="og:title" content="{esc(p["title"])}"><meta property="og:description" content="{esc(p["description"])}">'
        if p['noindex']:metadata+='<meta name="robots" content="noindex,follow">'
        if SITE_URL:
            canonical=SITE_URL+'/'+('' if path=='index.html' else path)
            metadata+=f'<link rel="canonical" href="{esc(canonical)}"><meta property="og:url" content="{esc(canonical)}">'
        if path=='404.html':
            # Relative links need an explicit deployment base when Pages serves 404
            # for arbitrary-depth URLs. With no configured domain, only the root
            # is assumed; project/custom-domain deployments get the base in CI.
            base=(urlsplit(SITE_URL).path.rstrip('/')+'/' if SITE_URL else '/')
            metadata+=f'<base href="{esc(base)}">'
        css=posixpath.relpath('assets/css/styles.css',posixpath.dirname(path) or '.')
        icon=posixpath.relpath('assets/favicon.svg',posixpath.dirname(path) or '.')
        document=f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["title"])}'+('' if path=='index.html' else ' · HallResearch.ai Library')+f'</title>{metadata}<link rel="stylesheet" href="{css}"><link rel="icon" href="{icon}" type="image/svg+xml"></head><body>{full}</body></html>\n'
        target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(document)
    (OUT/'.nojekyll').touch()
    robots='User-agent: *\nAllow: /\n'
    if SITE_URL:
        urls=[SITE_URL+'/'+('' if p=='index.html' else p) for p,v in PAGES.items() if not v['noindex']]
        sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(u)+'</loc></url>' for u in urls)+'</urlset>\n'
        (OUT/'sitemap.xml').write_text(sitemap)
        robots+='Sitemap: '+SITE_URL+'/sitemap.xml\n'
    (OUT/'robots.txt').write_text(robots)

def build_index():
    records=[];seen={}
    for path,page in PAGES.items():
        if page['noindex'] or not page['area'] or page['area'] in ('home','about'):continue
        area=page['area'];doc=html.parse(str(OUT/path));article=doc.xpath('//article[contains(@class,"prose")]')
        archived='archived' in path
        records.append({'title':page['title'],'url':path,'area':area,'section':page['title'],'summary':page['description'],'kind':'page','archived':archived})
        for article_node in article:
            heading=page['title']
            for node in article_node.iter():
                if node.tag in ('h2','h3','h4','h5','h6'):heading=text(node)
                if node.tag not in ('li','p','td'):continue
                if node.tag=='li' and node.xpath('./ul|./ol'):continue
                if not node.xpath('ancestor::*[@data-source-document]'):continue
                if node.tag in ('li','td') and node.xpath('./p'):continue
                for a in node.xpath('.//a[@href]'):
                    href=a.get('href');u=urlsplit(href);label=text(a)
                    if u.scheme not in ('http','https') or not label or a.xpath('.//img'):continue
                    if a.xpath('ancestor::*[contains(@class,"provenance") or contains(@class,"file-list")]'):continue
                    if label.startswith('https://') and node.tag=='p' and len(text(node))<40:continue
                    identity=(href.rstrip('/'),label.casefold())
                    context=page['title']+' · '+heading
                    ident=node.get('id')
                    if not ident:
                        position=node.getroottree().getpath(node)
                        ident='resource-'+hashlib.sha256((path+'|'+href+'|'+label+'|'+position).encode()).hexdigest()[:12]
                        node.set('id',ident)
                    location={'url':path+'#'+ident,'area':area,'section':page['title'],'subsection':heading,'archived':archived}
                    if identity in seen:
                        record=seen[identity]
                        if context not in record['contexts']:record['contexts'].append(context)
                        if location not in record['locations']:record['locations'].append(location)
                        if not archived:record['archived']=False
                        continue
                    record={'title':label,'url':path+'#'+ident,'resource_url':href,'area':area,'section':page['title'],'subsection':heading,'summary':text(node)[:280],'kind':'resource','contexts':[context],'locations':[location],'archived':archived}
                    records.append(record);seen[identity]=record
        (OUT/path).write_text('<!doctype html>\n'+html.tostring(doc.getroot(),encoding='unicode',method='html')+'\n')
    data=OUT/'assets/data';data.mkdir(parents=True,exist_ok=True)
    (data/'search-index.json').write_text(json.dumps(records,ensure_ascii=False,separators=(',',':'))+'\n')
    return records

def main():
    if SITE_URL and (urlsplit(SITE_URL).scheme!='https' or not urlsplit(SITE_URL).netloc):
        raise RuntimeError('SITE_URL must be the actual absolute HTTPS deployment URL.')
    init_sources();register_branch_urls();build_branches();build_guides();build_extra_documents();build_about();build_home();build_search_and_404();write_pages();index=build_index()
    verification=ROOT/'verification';verification.mkdir(exist_ok=True)
    (verification/'build-transformations.json').write_text(json.dumps(NOTES,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'content/document-map.json').write_text(json.dumps(DOC_URLS,ensure_ascii=False,indent=2)+'\n')
    summary={'source_checked_at_utc':MANIFEST['checked_at_utc'],'pages':len(PAGES),'search_entries':len(index),'resource_search_entries':sum(x['kind']=='resource' for x in index),'site_url':SITE_URL,'source_documents':len(DOCUMENTS)}
    (verification/'build-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
