/* EREDO family of brands. Shared footer strip. Served from https://eredo-house-eredo.static.hf.space/family.js
   To add a brand: add one line to BRANDS. Set live:true once its site returns 200. */
(function(){
  var BRANDS = [
    {name:"EREDO",   url:"https://eredo-house-eredo.static.hf.space/",   live:true},
    {name:"TENOR",   url:"https://eredo-house-tenor.static.hf.space/", live:true},
    {name:"GANTRY",  url:"https://eredo-house-gantry.static.hf.space/", live:true},
    {name:"SCATTO",  url:"https://eredo-house-scatto.static.hf.space/", live:true},
    {name:"LUCE",    url:"https://eredo-house-luce.static.hf.space/", live:true}
  ];
  function render(){
    var el=document.getElementById("family-strip"); if(!el) return;
    var here=location.hostname, items=BRANDS.filter(function(b){return b.live;});
    if(items.length<2){el.style.display="none";return;}
    el.innerHTML='<nav aria-label="The family" style="display:flex;justify-content:center;flex-wrap:wrap;gap:8px 36px;padding:18px 16px;border-top:1px solid rgba(176,141,87,.25);font:500 12px/1 Cinzel,\'Times New Roman\',serif;letter-spacing:.32em">'+
      items.map(function(b){var cur=b.url.indexOf(here)>-1;
        return '<a href="'+b.url+'"'+(cur?' aria-current="page"':'')+' style="color:inherit;opacity:'+(cur?1:.6)+';text-decoration:none;display:inline-flex;align-items:center;min-height:44px">'+b.name+'</a>';}).join("")+'</nav>';
  }
  if(document.readyState!=="loading") render(); else document.addEventListener("DOMContentLoaded",render);
})();
