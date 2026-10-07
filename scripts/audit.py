#!/usr/bin/env python3
"""Validate HTML, links, assets, search destinations, JSON and Pages structure."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
import xml.etree.ElementTree as ET
import html5lib
from lxml import html
import yaml

ROOT=Path(__file__).resolve().parents[1]
def audit(root):
 root=root.resolve();docs={p:html.parse(str(p)) for p in root.rglob('*.html')}
 errors=[];refs=0;anchors=0;html_checks=0
 def issue(page,url,reason):errors.append({'page':str(page.relative_to(root)),'url':url,'reason':reason})
 def check(page,value):
  nonlocal refs,anchors
  u=urlsplit(value)
  if u.scheme or u.netloc:return
  refs+=1
  target=root/unquote(u.path).lstrip('/') if u.path.startswith('/') else page.parent/unquote(u.path) if u.path else page
  if target.is_dir():target=target/'index.html'
  target=target.resolve()
  if not target.is_relative_to(root):issue(page,value,'path escapes public directory');return
  if not target.is_file():issue(page,value,'missing file');return
  if u.fragment and target in docs:
   anchors+=1
   if unquote(u.fragment) not in docs[target].xpath('//@id|//@name'):issue(page,value,'missing anchor')
 for page,doc in docs.items():
  ids=doc.xpath('//@id')
  for ident,n in Counter(ids).items():
   if n>1:issue(page,ident,'duplicate ID')
  if len(doc.xpath('//h1'))!=1:issue(page,'','page must contain one H1')
  if len(doc.xpath('//main'))!=1:issue(page,'','page must contain one main landmark')
  if not doc.xpath('//html[@lang="en"]'):issue(page,'','missing document language')
  if not doc.xpath('//title/text()') or not doc.xpath('//meta[@name="description"]/@content'):issue(page,'','missing title or meta description')
  levels=[int(h.tag[1]) for h in doc.xpath('//main//h1|//main//h2|//main//h3|//main//h4|//main//h5|//main//h6')]
  for a,b in zip(levels,levels[1:]):
   if b>a+1:issue(page,f'h{a} to h{b}','heading level skipped')
  for e in doc.xpath('//*[@href or @src or @action]'):
   if e.tag=='base':continue
   for attr in ('href','src','action'):
    value=e.get(attr)
    if value is not None:
     if urlsplit(value).scheme in ('javascript','data') and attr!='src':issue(page,value,'unsafe URL scheme')
     check(page,value)
  for img in doc.xpath('//img[not(@alt)]'):issue(page,img.get('src'),'image missing alt')
  for label in doc.xpath('//label[@for]'):
   if label.get('for') not in ids:issue(page,label.get('for'),'label target missing')
  parser=html5lib.HTMLParser(strict=False);parser.parse(page.read_text())
  html_checks+=1
  for pos,code,data in parser.errors:issue(page,f'{pos[0]}:{pos[1]}',f'HTML5 parse error: {code} {data}')
 for p in root.rglob('*.json'):
  try:json.loads(p.read_text())
  except Exception as exc:issue(p,'',f'invalid JSON: {exc}')
 for p in root.rglob('*.svg'):
  try:ET.parse(p)
  except Exception as exc:issue(p,'',f'invalid SVG: {exc}')
 for css in root.rglob('*.css'):
  for value in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text()):check(css,value)
 idx=json.loads((root/'assets/data/search-index.json').read_text())
 for entry in idx:
  check(root/'search.html',entry['url'])
  for loc in entry.get('locations',[]):check(root/'search.html',loc['url'])
  if urlsplit(entry['url']).scheme or entry['url'].startswith('/'):issue(root/'search.html',entry['url'],'search destination must be a site-relative content URL')
  if any(x in entry['url'] for x in ('content/','scripts/','.github/')):issue(root/'search.html',entry['url'],'maintenance metadata indexed')
 titles=[t.xpath('string(//title)') for t in docs.values()]
 if len(set(titles))!=len(titles):errors.append({'reason':'duplicate page titles'})
 if not (root/'.nojekyll').exists():errors.append({'reason':'missing .nojekyll'})
 sitemap=root/'sitemap.xml'
 if sitemap.exists():ET.parse(sitemap)
 workflow=yaml.load((ROOT/'.github/workflows/pages.yml').read_text(),Loader=yaml.BaseLoader)
 if set(('push','workflow_dispatch'))-workflow['on'].keys():errors.append({'reason':'Pages workflow missing triggers'})
 for perm in ('pages','id-token'):
  if workflow['jobs']['deploy']['permissions'].get(perm)!='write':errors.append({'reason':'Pages deployment missing permission '+perm})
 if workflow['jobs']['deploy'].get('needs')!='build':errors.append({'reason':'deployment must depend on checked build'})
 result={'pages':len(docs),'html5_documents_checked':html_checks,'internal_references_checked':refs,'anchor_references_checked':anchors,'search_entries':len(idx),'errors':errors,'passed':not errors}
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--site',type=Path,default=ROOT/'public');parser.add_argument('--report',type=Path,default=ROOT/'verification/internal-check.json');args=parser.parse_args()
 result=audit(args.site);args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='errors'},indent=2))
 for error in result['errors'][:30]:print(error)
 raise SystemExit(0 if result['passed'] else 1)
