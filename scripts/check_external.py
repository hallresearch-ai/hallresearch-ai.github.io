#!/usr/bin/env python3
"""Inventory every public external URL and HTTP-check a reproducible sample.

No upstream URL is replaced. HTTP errors and untested URLs remain explicit.
"""
import argparse,concurrent.futures,csv,datetime as dt,hashlib,json,re,socket,time
from collections import Counter,defaultdict
from pathlib import Path
import urllib.error,urllib.request
from urllib.parse import urlsplit,urldefrag,unquote
from lxml import html
ROOT=Path(__file__).resolve().parents[1]

def inventory():
 urls={};priority=[]
 for page in sorted((ROOT/'public').rglob('*.html')):
  doc=html.parse(str(page));p=str(page.relative_to(ROOT/'public'))
  for e in doc.xpath('//*[@href or @src]'):
   value=e.get('href') or e.get('src');u=urlsplit(value)
   if u.scheme not in ('http','https'):continue
   key=urldefrag(value)[0]
   urls.setdefault(key,{'url':key,'pages':[],'labels':[]})
   if p not in urls[key]['pages']:urls[key]['pages'].append(p)
   label=re.sub(r'\s+',' ',e.text_content()).strip()
   if label and label not in urls[key]['labels']:urls[key]['labels'].append(label)
  # First external resource under every heading, including countries.
  pending=True
  for e in doc.xpath('//main//*[self::h2 or self::h3 or self::h4 or self::h5 or self::a[@href]]'):
   if e.tag.startswith('h'):pending=True
   elif pending and urlsplit(e.get('href')).scheme in ('http','https'):
    priority.append(urldefrag(e.get('href'))[0]);pending=False
 return urls,list(dict.fromkeys(priority))

def tree_verified(url):
 u=urlsplit(url)
 if u.netloc not in ('github.com','raw.githubusercontent.com'):return False
 m=re.match(r'^/hallresearch-ai/([^/]+)/(?:blob/|tree/)?([a-f0-9]{40})/(.+)$',u.path)
 if not m:return False
 repo,sha,path=m.groups();folder=ROOT/'content/upstream'/repo
 if not folder.exists():return False
 meta=json.loads((folder/'repository.json').read_text());tree=json.loads((folder/'tree.json').read_text())
 return meta['commit']==sha and any(x['path']==unquote(path) for x in tree['tree'])

def check(item):
 url=item['url'];start=time.monotonic();request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; HallResearch-Library-LinkCheck/1.0)','Accept':'*/*'},method='GET')
 try:
  with urllib.request.urlopen(request,timeout=12) as response:
   body=response.read(8192);code=response.status;resolved=response.url
   challenge=any(term in body.lower() for term in (b'just a moment...',b'checking your browser',b'access denied',b'captcha'))
   status='uncertain_challenge' if challenge else 'reachable'
   result={'status':status,'http_status':code,'final_url':resolved,'detail':'Access challenge detected' if challenge else ''}
 except urllib.error.HTTPError as exc:
  code=exc.code
  status='http_404_or_410' if code in (404,410) else 'uncertain_http_error'
  result={'status':status,'http_status':code,'final_url':exc.url,'detail':str(exc.reason)}
 except Exception as exc:result={'status':'uncertain_network','http_status':'','final_url':'','detail':str(exc)[:180]}
 result['seconds']=round(time.monotonic()-start,2);return {**item,**result}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--sample',type=int,default=280);parser.add_argument('--all',action='store_true');parser.add_argument('--workers',type=int,default=12);args=parser.parse_args()
 urls,priority=inventory();selected=list(urls) if args.all else priority[:args.sample]
 ranked=sorted(set(urls)-set(selected),key=lambda x:hashlib.sha256(x.encode()).hexdigest())
 selected+=ranked[:max(0,args.sample-len(selected))]
 results={};tasks=[]
 for url,item in urls.items():
  if tree_verified(url):results[url]={**item,'status':'repository_tree_verified','http_status':'','final_url':url,'detail':'File path verified in the live commit-pinned public GitHub tree; no separate HTTP request.'}
  elif url in selected:tasks.append(item)
  else:results[url]={**item,'status':'not_checked','http_status':'','final_url':'','detail':'Outside the reproducible HTTP sample.'}
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
  for i,result in enumerate(pool.map(check,tasks),1):
   results[result['url']]=result
   if i%25==0:print(f'HTTP checks: {i}/{len(tasks)}',flush=True)
 report={'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'unique_urls':len(urls),'http_checks':len(tasks),'status_counts':dict(Counter(x['status'] for x in results.values())),'urls':list(results.values())}
 out=ROOT/'verification';out.mkdir(exist_ok=True)
 (out/'external-links.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 fields=['url','status','http_status','final_url','detail','pages','labels']
 for name,rows in [('external-url-inventory.csv',results.values()),('external-urls-broken-or-uncertain.csv',[x for x in results.values() if x['status'] not in ('reachable','repository_tree_verified')])]:
  with (ROOT/name).open('w',newline='') as stream:
   writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader()
   for row in rows:writer.writerow({**row,'pages':' | '.join(row['pages']),'labels':' | '.join(row['labels'])})
 print(json.dumps({k:v for k,v in report.items() if k!='urls'},indent=2),flush=True)
