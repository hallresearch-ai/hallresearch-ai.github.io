#!/usr/bin/env python3
"""Independently compare source text blocks and external links with published HTML."""
from collections import Counter
from copy import deepcopy
import json,re,subprocess
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'content/source-manifest.json').read_text())
sources={item['repo']+'/'+f['path']:(ROOT/'content/upstream'/item['repo']/f['path']).read_text() for item in manifest['repositories'] for f in item['files'] if f['path'].lower().endswith('.md')}
raw=json.loads(subprocess.run(['node','scripts/render-markdown.mjs'],input=json.dumps(sources),text=True,capture_output=True,check=True,cwd=ROOT).stdout)
documents={k:html.fragment_fromstring(v,create_parent='div') for k,v in raw.items()}
# Ignore only the decorative badge separator removed from public presentation.
for document in documents.values():
 for img in document.xpath('.//img'):
  if 'img.shields.io/' in img.get('src','') and not img.get('alt'):
   previous=img.getprevious()
   if previous is not None and previous.tail:
    previous.tail=re.sub(r'\s*\|\s*$', '', previous.tail)
actual={key:[] for key in sources}
for page in (ROOT/'public').rglob('*.html'):
 doc=html.parse(str(page))
 for fragment in doc.xpath('//*[@data-source-document]'):
  fragment=deepcopy(fragment)
  for badge in list(fragment.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," badge ")]')):
   badge.text=''
  actual[fragment.get('data-source-document')].append(fragment)
def normal(value):
 value=re.sub(r'\[!(\w+)\]',lambda m:m.group(1).title()+'.',value)
 value=value.replace('☑','').replace('☐','')
 value=re.sub(r'\s+',' ',value).strip()
 return value.rstrip(' |')
def blocks(nodes):
 result=Counter();code=Counter();links=Counter()
 for node in nodes:
  for e in node.xpath('.//p|.//li|.//th|.//td|.//pre'):
   value=normal(e.text_content())
   if value:result[(e.tag,value)]+=1
   if e.tag=='pre':code[e.text_content()]+=1
  for a in node.xpath('.//a[@href]'):
   u=urlsplit(a.get('href'))
   # Local navigation can replace source cross-links between Library repositories.
   if u.scheme in ('https','http') and not (u.netloc=='github.com' and re.fullmatch(r'/hallresearch-ai(?:/[^/]+)?/?',u.path)):
    links[(normal(a.text_content()),a.get('href'))]+=1
 return result,code,links
results=[]
for key,doc in documents.items():
 expected,expected_code,expected_links=blocks([doc]);published,published_code,published_links=blocks(actual[key])
 missing=expected-published;missing_code=expected_code-published_code;missing_links=expected_links-published_links
 result={'source_document':key,'source_text_blocks':sum(expected.values()),'source_code_blocks':sum(expected_code.values()),'source_external_links':sum(expected_links.values()),'missing_text_blocks':[{'tag':tag,'text':value,'count':count} for (tag,value),count in missing.items()],'missing_code_blocks':list(missing_code.elements()),'missing_external_links':[{'label':label,'url':url,'count':count} for (label,url),count in missing_links.items()]}
 results.append(result)
summary={'source_documents':len(results),'text_blocks':sum(r['source_text_blocks'] for r in results),'code_blocks':sum(r['source_code_blocks'] for r in results),'external_links':sum(r['source_external_links'] for r in results),'missing_text_blocks':sum(len(r['missing_text_blocks']) for r in results),'missing_code_blocks':sum(len(r['missing_code_blocks']) for r in results),'missing_external_links':sum(len(r['missing_external_links']) for r in results)}
report={**summary,'documents':results,'passed':not any(summary[k] for k in ('missing_text_blocks','missing_code_blocks','missing_external_links'))}
(ROOT/'verification/content-fidelity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for r in results:
 if r['missing_text_blocks'] or r['missing_code_blocks'] or r['missing_external_links']:print(json.dumps(r,ensure_ascii=False)[:6000])
raise SystemExit(0 if report['passed'] else 1)
