// CI: fail if any look points to a LINKS key that does not exist.
const fs=require('fs'),vm=require('vm'),path=require('path');
const src=fs.readFileSync(path.join(__dirname,'..','data','looks.js'),'utf8');
const ctx={window:{}};vm.runInNewContext(src,ctx);
const D=ctx.window.KW_LOOKS;let bad=0;
if(!D||typeof D.LINKS!=='object'||!Array.isArray(D.LOOKS)){console.error('looks.js: KW_LOOKS missing LINKS or LOOKS');process.exit(1)}
for(const lk of D.LOOKS){for(const k of lk.pieces||[]){if(!D.LINKS[k]){console.error(`Look "${lk.id}" points to missing LINKS key "${k}"`);bad++}}
  for(const k of lk.pieces||[]){const p=D.LINKS[k];if(p&&(!p.url||!/^https:\/\//.test(p.url))){console.error(`LINKS "${k}" has no https url`);bad++}
  if(p&&p.img&&!/^https?:/.test(p.img)&&!fs.existsSync(path.join(__dirname,'..',p.img))){console.error(`LINKS "${k}" image missing: ${p.img}`);bad++}}}
if(bad){console.error(bad+' problem(s)');process.exit(1)}
console.log(`looks ok: ${D.LOOKS.length} looks, ${Object.keys(D.LINKS).length} links`);
