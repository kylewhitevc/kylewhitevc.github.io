// CI: validate links/data/looks.js against the EREDO looks.json contract.
// Run locally before every push: python3 deploy.py <files> (the gate). CI only re-checks, quietly.
// Fails on: a look pointing to a missing links key, a non-https url, a missing local image,
// a missing/invalid price, or a was (original) price below the now price.
const fs=require('fs'),vm=require('vm'),path=require('path');
const src=fs.readFileSync(path.join(__dirname,'..','data','looks.js'),'utf8');
const ctx={window:{}};vm.runInNewContext(src,ctx);
const D=ctx.window.KW_LOOKS;let bad=0;const err=m=>{console.error(m);bad++};
if(!D||typeof D.links!=='object'||!Array.isArray(D.looks)){console.error('looks.js: KW_LOOKS needs links{} and looks[]');process.exit(1)}
for(const lk of D.looks){
  if(!Array.isArray(lk.pieces)||!lk.pieces.length)err(`Look "${lk.id}" has no pieces`);
  for(const k of lk.pieces||[]){
    const p=D.links[k];
    if(!p){err(`Look "${lk.id}" points to missing links key "${k}"`);continue}
    if(!p.url||!/^https:\/\//.test(p.url))err(`links "${k}" has no https url`);
    if(!(typeof p.price==='number'&&p.price>0))err(`links "${k}" has no valid price`);
    if(p.was!=null&&!(typeof p.was==='number'&&p.was>=p.price))err(`links "${k}" was ${p.was} is below price ${p.price}`);
    if(p.img&&!/^https?:/.test(p.img)&&!fs.existsSync(path.join(__dirname,'..',p.img)))err(`links "${k}" image missing: ${p.img}`);
  }
}
if(bad){console.error(bad+' problem(s)');process.exit(1)}
console.log(`looks ok: ${D.looks.length} looks, ${Object.keys(D.links).length} links`);
