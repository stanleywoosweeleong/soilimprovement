// extra states for the recipe builder
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1380,height:900}});
await p.goto('file://'+process.argv[2]+'#liquid-fertilizer');await p.waitForTimeout(600);
await p.evaluate(()=>document.querySelector('#langs button[data-lang="en"]').click());
const all=new Set();const grab=async()=>{(await p.evaluate(()=>window.__i18nKeys())).forEach(k=>all.add(k))};
await grab();
for(const pr of ['High-N','High-P','High-K']){
 await p.evaluate(pr=>document.querySelector('#lb-presets button[data-p="'+pr+'"]').click(),pr);await grab();
 for(const st of [[0,null,null,null,0,0],[null,0,0,0,20,null],[30,30,30,30,12,2],[null,null,null,null,null,null]]){
  await p.evaluate(st=>{st.forEach((v,i)=>{if(v!==null)document.getElementById('lb-a'+i).value=v});document.getElementById('lb-rows').dispatchEvent(new Event('input'))},st);await grab();}
 await p.selectOption('#lb-s3','sea');await p.evaluate(()=>{document.getElementById('lb-a3').value=5;document.getElementById('lb-rows').dispatchEvent(new Event('input'))});await grab();
 await p.selectOption('#lb-s3','wash');
}
await p.evaluate(()=>{const v=document.getElementById('lf-vol');v.value=0;v.dispatchEvent(new Event('input'))});await grab();
const prev=JSON.parse(require('fs').readFileSync(process.argv[3]));
require('fs').writeFileSync(process.argv[3],JSON.stringify([...new Set([...prev,...all])].sort(),null,1));
console.log('total',new Set([...prev,...all]).size);await b.close()})();
