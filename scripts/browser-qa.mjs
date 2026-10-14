import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {chromium} from 'playwright';

const root=process.cwd(), executablePath=process.env.BROWSER_EXECUTABLE;
const directory=process.env.QA_DIRECTORY || path.join(root,'public');
const basePath=process.env.QA_BASE_PATH || '';
const port=Number(process.env.QA_PORT || 8766);
const origin=`http://127.0.0.1:${port}`, base=origin+basePath+'/';
const server=spawn('python3',['scripts/preview.py','--port',String(port),'--directory',directory,'--base-path',basePath],{cwd:root});
await new Promise((resolve,reject)=>{server.stdout.once('data',resolve);server.once('exit',code=>reject(new Error(`Preview server exited ${code}`)));});
let browser;
const results={pages:[],searches:[],keyboard:[],errors:[],accessibility:[],subpath:basePath,viewports:[1440,1280,768,375,320]};
const samples=['index.html','governance/government-and-multilateral-ai-policy-guidance.html','assessment/technical-resources.html','guides/index.html','cite.html','search.html'];
function pages(folder){return fs.readdirSync(folder,{withFileTypes:true}).flatMap(x=>x.isDirectory()?pages(path.join(folder,x.name)):x.name.endsWith('.html')?[path.relative(directory,path.join(folder,x.name)).replaceAll(path.sep,'/')]:[]);}
try {
 browser=await chromium.launch({...(executablePath?{executablePath}:{}),headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 page.on('pageerror',error=>results.errors.push({kind:'pageerror',url:page.url(),message:error.message}));
 page.on('response',response=>{if(response.url().startsWith(origin) && response.status()>=400 && !response.url().includes('nonexistent'))results.errors.push({kind:'HTTP',url:response.url(),status:response.status()});});
 const axeSource=fs.readFileSync(path.join(root,'node_modules/axe-core/axe.min.js'),'utf8');
 for (const route of pages(directory).sort()) {
  await page.goto(base+route,{waitUntil:'load'});
  await page.addScriptTag({content:axeSource});
  const a=await page.evaluate(async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),incomplete:r.incomplete.map(v=>({id:v.id,nodes:v.nodes.length}))};});
  results.accessibility.push({route,width:1440,...a});
  const layout=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth,heading:document.querySelector('h1').textContent}));
  results.pages.push({route,width:1440,...layout});
  if(samples.includes(route)) {
   for(const width of [1280,768,375,320]) {
    await page.setViewportSize({width,height:900});
    results.pages.push({route,width,...await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth}))});
   }
   await page.setViewportSize({width:375,height:812});
   const mobileA=await page.evaluate(async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),incomplete:r.incomplete.map(v=>({id:v.id,nodes:v.nodes.length}))};});
   results.accessibility.push({route,width:375,...mobileA});
   await page.screenshot({path:path.join(root,'verification',route.replaceAll('/','-')+'-mobile.png')});
   await page.setViewportSize({width:1440,height:1000});
   if(route==='index.html' || route==='guides/index.html')await page.screenshot({path:path.join(root,'verification',route.replaceAll('/','-')+'-desktop.png')});
  }
  console.log('Checked '+route);
 }
 for(const q of ['prompt injection','red teaming','AI incidents','labor','NIST AI RMF','explainability','university policy']) {
  await page.goto(base+'search.html?q='+encodeURIComponent(q));
  await page.waitForFunction(()=>/results?\./.test(document.querySelector('#search-status').textContent));
  const count=await page.locator('.result').count();const destinations=await page.locator('.result h2 a').evaluateAll(nodes=>nodes.slice(0,5).map(n=>n.getAttribute('href')));
  results.searches.push({query:q,status:await page.locator('#search-status').innerText(),count,destinations});
  if(!count)throw new Error('No results for '+q);
 }
 await page.goto(base+'search.html?q=prompt+injection');
 await page.waitForSelector('.result h2 a');
 await page.locator('.result h2 a').first().click();
 const hash=new URL(page.url()).hash.slice(1);
 if(hash&&!await page.evaluate(id=>!!document.getElementById(id),hash))throw new Error('Resource anchor does not exist');
 results.keyboard.push({check:'resource result navigation',passed:true});
 await page.goto(base+'search.html?q=labor');await page.waitForSelector('.result');
 const before=await page.locator('.result').count();await page.locator('#more-results').click();
 const after=await page.locator('.result').count();if(after<=before)throw new Error('Search pagination failed');
 await page.locator('#area').selectOption('assessment');await page.waitForTimeout(180);
 results.searches.push({query:'labor, Assessment filter',status:await page.locator('#search-status').innerText()});
 await page.locator('#q').fill('zzzznosuchresource987');await page.locator('#q').press('Enter');
 if(!/No results/.test(await page.locator('#search-status').innerText()))throw new Error('No-result state failed');
 await page.route('**/assets/data/search-index.json',route=>route.abort());
 await page.goto(base+'search.html?q=labor');await page.waitForSelector('#retry-search:visible');
 await page.unroute('**/assets/data/search-index.json');await page.locator('#retry-search').click();await page.waitForSelector('.result');
 results.keyboard.push({check:'search fetch failure and retry',passed:true});
 await page.setViewportSize({width:375,height:812});await page.goto(base+'index.html');
 await page.locator('.mobile-toggle').click();if(await page.locator('.mobile-toggle').getAttribute('aria-expanded')!=='true')throw new Error('Menu did not expand');
 await page.keyboard.press('Escape');if(await page.locator('.mobile-toggle').getAttribute('aria-expanded')!=='false')throw new Error('Escape did not close menu');
 if(!await page.locator('.mobile-toggle').evaluate(e=>e===document.activeElement))throw new Error('Escape did not restore focus');
 results.keyboard.push({check:'mobile menu state and Escape focus',passed:true});
 await page.goto(base+'index.html');await page.keyboard.press('Tab');
 if(!await page.locator('.skip-link').evaluate(e=>e===document.activeElement))throw new Error('Skip link is not first in tab order');
 await page.keyboard.press('Enter');if(await page.evaluate(()=>document.activeElement.id)!=='main-content')throw new Error('Skip navigation did not move focus');
 results.keyboard.push({check:'keyboard skip navigation',passed:true});
 await page.emulateMedia({reducedMotion:'reduce'});
 const motion=await page.locator('.catalog-row').first().evaluate(e=>getComputedStyle(e).transitionDuration);if(motion!=='0s')throw new Error('Reduced motion styling failed');
 const response=await page.goto(base+'nonexistent/deep/page.html');
 if(response.status()!==404||!await page.locator('h1').innerText().then(x=>x.includes('Page not found')))throw new Error('Custom 404 failed');
 await page.locator('a.button').click();if(new URL(page.url()).pathname!==(basePath||'')+'/index.html')throw new Error('404 return link escaped base path');
 results.keyboard.push({check:'deep URL 404 navigation',passed:true});
 const noJS=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:812}});const fallback=await noJS.newPage();await fallback.goto(base+'index.html');
 if(!await fallback.locator('#main-navigation').isVisible())throw new Error('Navigation inaccessible without JS');
 await fallback.goto(base+'search.html');if(!await fallback.locator('noscript').isVisible())throw new Error('Search no-script fallback absent');
 await noJS.close();results.keyboard.push({check:'no-JavaScript navigation and search fallback',passed:true});
} catch(error) {results.errors.push({kind:'test failure',message:error.message});}
finally {if(browser)await browser.close();server.kill();}
results.overflow=results.pages.filter(x=>x.width>x.viewport+1);
results.violation_count=results.accessibility.reduce((n,x)=>n+x.violations.length,0);
results.passed=!results.errors.length&&!results.overflow.length&&!results.violation_count;
const target=path.join(root,'verification',basePath?'browser-subpath-check.json':'browser-check.json');
fs.writeFileSync(target,JSON.stringify(results,null,2)+'\n');
console.log(JSON.stringify({pages:results.pages.length,accessibility_runs:results.accessibility.length,violations:results.violation_count,errors:results.errors,overflow:results.overflow,passed:results.passed},null,2));
process.exitCode=results.passed?0:1;
