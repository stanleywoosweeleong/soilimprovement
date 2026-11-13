const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1380,height:900}});const errs=[];p.on('pageerror',x=>errs.push(x.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(600);
const all=new Set();const grab=async()=>{(await p.evaluate(()=>window.__i18nKeys())).forEach(k=>all.add(k))};
await grab();
// toggles
for(const sel of ['.xall','.tbl-toggle']){const n=await p.locator(sel).count();for(let i=0;i<n;i++){await p.locator(sel).nth(i).evaluate(e=>e.click())}}
await grab();
// checker states
const sets=[{ec:3.41,ph:7.48,om:1.66,p:345,k:335,ca:5926,mg:2354},{ec:0.12,ph:4.6,om:1.4,p:6,k:45,ca:280,mg:22},{ec:0.05},{ec:0.15},{ec:0.25},{ec:0.35},{ec:0.5},{ec:2.5,ph:8.5,om:0.5,p:500,k:400},{ph:4.2,p:5,k:20,ca:300,mg:30,om:4},{ph:6,om:3.5,p:30,k:60,ca:800,mg:70},{}];
for(const st of sets){await p.evaluate(st=>{['ec','ph','om','p','k','ca','mg'].forEach(k=>{document.getElementById('in-'+k).value=st[k]!=null?st[k]:''});document.getElementById('soilform').dispatchEvent(new Event('input'))},st);await p.waitForTimeout(50);await grab()}
await p.evaluate(()=>{const q=document.getElementById('gl-q');q.value='zzzzqq';q.dispatchEvent(new Event('input'))});await grab();
await p.evaluate(()=>{window.scrollTo(0,3000);window.dispatchEvent(new Event('scroll'))});await grab();
require('fs').writeFileSync(process.argv[3],JSON.stringify([...all].sort(),null,1));
console.log('keys',all.size,'chars',[...all].join('').length,'errors',errs);await b.close()})();
