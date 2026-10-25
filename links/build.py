#!/usr/bin/env python3
"""Builds index.html for kylewhitevc.github.io/links.

Data lives in three files, so content changes never need a redesign:
  data/ticker.json  - the scrolling deals strip (EREDO / SECONDO items)
  data/links.json   - profile links and featured houses
  link_map.csv      - "What I wear" picks. Fill affiliate_url when a network approves; it replaces url.
Run: python3 build.py   then deploy index.html (+ img/) to links/ in kylewhitevc/kylewhitevc.github.io.
"""
import csv, html, json, os

D = os.path.dirname(os.path.abspath(__file__))
e = html.escape
ticker = json.load(open(os.path.join(D, 'data/ticker.json')))['items']
L = json.load(open(os.path.join(D, 'data/links.json')))
picks = list(csv.DictReader(open(os.path.join(D, 'link_map.csv'))))


def money(v):
    v = float(v)
    return f"${v:,.0f}"


def tick_items(hidden=False):
    out = []
    for t in ticker:
        attrs = ' tabindex="-1" aria-hidden="true"' if hidden else ''
        out.append(
            f'<a class="tk" href="{e(t["url"])}" target="_blank" rel="noopener"{attrs}>'
            f'<b>{e(t["house"])}</b><span class="m">{e(t["maker"])}</span>'
            f'<span class="pc">{e(t["piece"])}</span><span class="pr">{money(t["price"])}</span>'
            f'<span class="off">&minus;{int(t["pct"])}%</span></a>')
    return ''.join(out)


links_html = ''.join(
    f'''<a class="row" href="{e(l['url'])}" target="_blank" rel="noopener">
      <span class="rl">{e(l['label'])}</span><span class="rs">{e(l['sub'])}</span><span class="ar" aria-hidden="true">&rarr;</span></a>'''
    for l in L['links'])

house = next((h for h in L['houses'] if h.get('url')), None)
deals = sorted(ticker, key=lambda t: -int(t['pct']))
deals_html = ''.join(
    f"""<a class="deal {e(t['house'].lower())}" href="{e(t['url'])}" target="_blank" rel="sponsored noopener">
      <span class="dimg"><img src="{e(t['img'])}" width="600" height="750" alt="{e(t['maker'])} {e(t['piece'])}" loading="lazy" decoding="async"><span class="badge">&minus;{int(t['pct'])}%</span><span class="hs">{e(t['house'])}</span></span>
      <span class="dm">{e(t['maker'])}</span><span class="dn">{e(t['piece'])}</span>
      <span class="dp"><b>{money(t['price'])}</b><s>{money(t['was'])}</s></span></a>"""
    for t in deals)
houses_n = {h: sum(1 for t in deals if t['house'] == h) for h in ('EREDO', 'SECONDO')}

def origin(m):
    return 'Made in ' + m.split('(')[0].strip()

feat, rest = picks[0], picks[1:]
def href(r):
    return e(r['affiliate_url'].strip() or r['url'])
feat_html = f"""<a class="feat" href="{href(feat)}" target="_blank" rel="sponsored noopener">
  <img src="img/{e(feat['id'])}.webp" width="900" height="1125" alt="{e(feat['brand'])} {e(feat['name'])}" loading="lazy" decoding="async">
  <span class="fo"><span class="no">N&deg;01</span><span class="pb">{e(feat['brand'])} &middot; {e(origin(feat['made_in']))}</span>
  <span class="fn">{e(feat['name'])}</span><span class="fp">{money(feat['price'])}<i>Shop &rarr;</i></span></span></a>"""
picks_html = ''.join(
    f"""<a class="pick" href="{href(r)}" target="_blank" rel="sponsored noopener">
      <span class="ph"><img src="img/{e(r['id'])}.webp" width="600" height="750" alt="{e(r['brand'])} {e(r['name'])}" loading="lazy" decoding="async"><span class="no">N&deg;{i:02d}</span></span>
      <span class="pc">{e(r['category'])}</span><span class="pb">{e(r['brand'])}</span><span class="pn">{e(r['name'])}</span>
      <span class="pf"><span class="pp">{money(r['price'])}</span><span class="po">{e(origin(r['made_in']))}</span></span></a>"""
    for i, r in enumerate(rest, 2))

CSS = r"""
:root{--bg:#0e0b09;--bg2:#17120e;--ink:#efe7da;--mute:#a3978a;--brass:#c3a165;--brass2:#e2c88f;--line:rgba(195,161,101,.22)}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;background:var(--bg)}
body{background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none;-webkit-tap-highlight-color:rgba(195,161,101,.15)}
.serif{font-family:"Cormorant Garamond","Cormorant",Garamond,"Times New Roman",serif}
.cap{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--brass)}
/* ticker */
.ticker{position:sticky;top:0;z-index:10;background:#070504;border-bottom:1px solid var(--line);overflow:hidden;height:38px}
.track{display:flex;width:max-content;animation:run 55s linear infinite}
.ticker:hover .track,.ticker:focus-within .track{animation-play-state:paused}
.tk{display:flex;align-items:center;gap:8px;height:38px;padding:0 22px;white-space:nowrap;font-size:12.5px;color:var(--ink);border-right:1px solid var(--line)}
.tk b{font-weight:600;letter-spacing:.2em;font-size:10.5px;color:var(--brass)}
.tk .m{color:var(--ink);font-weight:500}.tk .pc{color:var(--mute)}.tk .pr{font-variant-numeric:tabular-nums}
.tk .off{color:#0e0b09;background:var(--brass);font-weight:700;font-size:11px;padding:2px 6px;border-radius:2px}
@keyframes run{to{transform:translateX(-50%)}}
/* hero */
.hero{position:relative;max-width:1080px;margin:0 auto}
.hero figure{position:relative;height:min(118vw,560px);overflow:hidden}
.hero img{width:100%;height:100%;object-fit:cover;object-position:50% 18%;filter:sepia(.12) saturate(.9);transform:scale(1.06);animation:settle 2.4s cubic-bezier(.2,.7,.2,1) forwards}
.hero figure:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,11,9,0) 35%,rgba(14,11,9,.55) 68%,var(--bg) 100%)}
.intro{position:relative;margin-top:-150px;padding:0 24px;z-index:2}
h1{font-weight:500;font-size:58px;line-height:.95;letter-spacing:-.01em}
h1 i{color:var(--brass2);font-weight:400}
.lede{margin-top:16px;font-size:21px;line-height:1.35;color:var(--ink);max-width:30ch;font-style:italic}
.facts{margin-top:14px;color:var(--mute);font-size:13.5px;max-width:40ch}
@keyframes settle{to{transform:scale(1)}}
.rise{opacity:0;transform:translateY(14px);animation:rise .9s .25s cubic-bezier(.2,.7,.2,1) forwards}
.d2{animation-delay:.45s}.d3{animation-delay:.65s}
@keyframes rise{to{opacity:1;transform:none}}
main{max-width:1080px;margin:0 auto;padding:0 24px 40px}
section{margin-top:52px}
.sh{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:6px}
.sh h2{font-weight:500;font-size:30px;font-style:italic}
/* rows */
.row{display:grid;grid-template-columns:1fr auto;grid-template-areas:"l a" "s a";padding:18px 2px;border-bottom:1px solid var(--line);min-height:64px;align-items:center}
.rl{grid-area:l;font-family:"Cormorant Garamond",Garamond,serif;font-size:25px;line-height:1.1}
.rs{grid-area:s;color:var(--mute);font-size:13px;margin-top:2px}
.ar{grid-area:a;color:var(--brass);font-size:22px;transition:transform .3s}
.row:hover .ar,.row:focus-visible .ar{transform:translateX(5px)}
/* stage */
.stage{margin-top:26px}
.stage img{display:block;width:100%;height:auto;aspect-ratio:5/4;object-fit:cover;filter:sepia(.1) saturate(.92)}
.stage figcaption{margin-top:9px;font-family:"Cormorant Garamond",Garamond,serif;font-style:italic;font-size:16px;color:var(--mute)}
/* vault */
.vault{margin-top:64px;position:relative}
.vk{display:flex;align-items:flex-end;justify-content:space-between;gap:12px}
.vt{font-weight:500;font-size:52px;line-height:.9;font-style:italic}
.vt small{display:block;font-style:normal;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-bottom:12px}
.big{font-family:"Cormorant Garamond",Garamond,serif;font-size:70px;line-height:.8;color:transparent;-webkit-text-stroke:1px var(--brass);font-weight:500;letter-spacing:-.02em;white-space:nowrap}
.big sup{font-size:.42em;vertical-align:top;-webkit-text-stroke:0;color:var(--brass);margin-left:2px}
.vsub{margin-top:14px;color:var(--mute);font-size:14px;max-width:36ch}
.chips{display:flex;gap:8px;margin:22px 0 4px}
.chips input{position:absolute;opacity:0;pointer-events:none}
.chips label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;padding:9px 14px;border:1px solid var(--line);border-radius:40px;color:var(--mute);cursor:pointer;transition:.25s}
.chips label span{opacity:.6;margin-left:4px}
#f-all:checked~.chips [for=f-all],#f-eredo:checked~.chips [for=f-eredo],#f-secondo:checked~.chips [for=f-secondo]{background:var(--brass);color:#0e0b09;border-color:var(--brass)}
#f-eredo:checked~.rail .deal:not(.eredo),#f-secondo:checked~.rail .deal:not(.secondo){display:none}
.fx{position:absolute;opacity:0;pointer-events:none}
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:64%;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;margin:14px -24px 0;padding:4px 24px 8px;scroll-padding:0 24px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.rail::-webkit-scrollbar{display:none}
.deal{display:block;scroll-snap-align:start}
.dimg{position:relative;display:block;aspect-ratio:4/5;background:#ece5d9;overflow:hidden}
.dimg img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.deal:hover .dimg img{transform:scale(1.05)}
.badge{position:absolute;top:10px;left:10px;background:#0e0b09;color:var(--brass2);font-family:"Cormorant Garamond",Garamond,serif;font-size:22px;line-height:1;padding:6px 9px 5px;font-weight:500}
.hs{position:absolute;bottom:10px;right:10px;font-size:9.5px;letter-spacing:.28em;color:#3a2f25;font-weight:600}
.dm{display:block;margin-top:12px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.dn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:21px;line-height:1.12;margin-top:3px}
.dp{display:flex;gap:10px;align-items:baseline;margin-top:5px;font-variant-numeric:tabular-nums}
.dp b{font-weight:600;font-size:15px}.dp s{color:var(--mute);font-size:13px}
.swipe{margin-top:10px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}
/* house banner */
.house{display:grid;grid-template-columns:1fr 112px;gap:18px;align-items:center;margin-top:28px;padding:18px;border:1px solid var(--line);background:linear-gradient(120deg,#1b150f,#100c09);transition:border-color .3s}
.house:hover{border-color:var(--brass)}
.house img{width:112px;height:140px;object-fit:cover;display:block}
.hn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:32px;letter-spacing:.34em;font-weight:500;line-height:1}
.hl{display:block;margin-top:8px;font-size:13.5px;color:var(--mute)}
.hc{display:block;margin-top:12px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--brass);font-weight:600}
/* uniform */
.uni{margin-top:72px}
.ulede{margin-top:12px;color:var(--mute);font-size:14px;max-width:38ch}
.feat{position:relative;display:block;margin:22px -24px 0;overflow:hidden;aspect-ratio:4/5;background:#e2ddd3}
.feat img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.4s cubic-bezier(.2,.7,.2,1)}
.feat:hover img{transform:scale(1.03)}
.fo{position:absolute;left:0;right:0;bottom:0;padding:90px 24px 22px;background:linear-gradient(180deg,rgba(14,11,9,0),rgba(14,11,9,.88))}
.fo .no{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-style:italic;color:var(--brass2);font-size:18px}
.fo .pb{display:block;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink);opacity:.85;margin-top:4px}
.fn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:40px;line-height:1;margin-top:6px}
.fp{display:flex;justify-content:space-between;align-items:baseline;margin-top:10px;font-size:15px;font-variant-numeric:tabular-nums}
.fp i{font-style:normal;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--brass2)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px 14px;margin-top:30px}
.pick{display:block}
.ph{position:relative;display:block;overflow:hidden;background:#ece5d9;aspect-ratio:4/5}
.ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.pick:hover .ph img{transform:scale(1.05)}
.ph .no{position:absolute;top:8px;left:10px;font-family:"Cormorant Garamond",Garamond,serif;font-style:italic;font-size:15px;color:#5a4a3a}
.pc{display:block;margin-top:11px;font-size:9.5px;letter-spacing:.26em;text-transform:uppercase;color:var(--mute)}
.pb{display:block;margin-top:4px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.pn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:20px;line-height:1.12;margin-top:3px}
.pf{display:flex;justify-content:space-between;align-items:baseline;margin-top:6px;padding-top:7px;border-top:1px solid var(--line);font-size:12px;color:var(--mute)}
.pp{color:var(--ink);font-size:14px;font-variant-numeric:tabular-nums}
.po{font-size:10.5px;letter-spacing:.06em}
footer{max-width:1080px;margin:0 auto;padding:28px 24px 48px;border-top:1px solid var(--line);color:var(--mute);font-size:12px;line-height:1.6}
footer .sig{font-family:"Cormorant Garamond",Garamond,serif;font-style:italic;font-size:22px;color:var(--brass2);margin-bottom:8px}
:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
@media (min-width:760px){
 .hero{display:grid;grid-template-columns:1fr 1fr;align-items:end;gap:40px;padding:48px 24px 0}
 .hero figure{height:600px}
 .hero figure:after{background:linear-gradient(180deg,rgba(14,11,9,0) 70%,rgba(14,11,9,.4))}
 .intro{margin:0 0 30px;padding:0}
 h1{font-size:92px}
 .cols{display:grid;grid-template-columns:1fr 1fr;gap:48px}
 .rail{grid-auto-columns:calc((100% - 42px)/4);margin:14px 0 0;padding:4px 0 8px}
 .swipe{display:none}
 .vt{font-size:72px}.big{font-size:120px}
 .uwrap{display:grid;grid-template-columns:5fr 7fr;gap:36px;align-items:start}
 .feat{margin:22px 0 0;position:sticky;top:60px}
 .grid{grid-template-columns:repeat(2,1fr);gap:34px 22px}
}
@media (prefers-reduced-motion:reduce){
 *{animation:none!important;transition:none!important}
 .rise{opacity:1;transform:none}.hero img{transform:none}
 .ticker{overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
 .track .dup{display:none}
}
"""

VERIFIED = 'Oct 24, 2026'
house_html = (f'''<a class="house" href="{e(house['url'])}" target="_blank" rel="noopener"><span><span class="hn">{e(house['name'])}</span><span class="hl">{e(house['line'])}</span><span class="hc">Enter the full shop &rarr;</span></span><img src="{e(house['img'])}" width="112" height="140" alt="" loading="lazy"></a>''' if house else '')
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Kyle White</title>
<meta name="description" content="Kyle White: accelerator builder and venture investor from Youngstown, Ohio. LinkedIn, my site, and the Italian menswear I wear.">
<link rel="canonical" href="https://kylewhitevc.github.io/links/">
<meta property="og:type" content="profile">
<meta property="og:title" content="Kyle White">
<meta property="og:description" content="Accelerator builder, venture investor, and the menswear I actually wear.">
<meta property="og:image" content="https://kylewhitevc.github.io/links/img/kyle-og.jpg">
<meta property="og:url" content="https://kylewhitevc.github.io/links/">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#070504">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap">
<link rel="preload" as="image" href="img/kyle-hero.webp">
<style>{CSS}</style>
</head>
<body>
<nav class="ticker" aria-label="Today's markdowns from EREDO and SECONDO">
  <div class="track"><div style="display:flex">{tick_items()}</div><div class="dup" style="display:flex">{tick_items(True)}</div></div>
</nav>
<header class="hero">
  <figure><img src="img/kyle-hero.webp" width="752" height="940" alt="Kyle White" fetchpriority="high"></figure>
  <div class="intro">
    <p class="cap rise">Youngstown, Ohio</p>
    <h1 class="serif rise d2">Kyle <i>White</i></h1>
    <p class="lede serif rise d3">I build accelerators and back founders. Off the clock, it&rsquo;s Italian cashmere and good leather.</p>
    <p class="facts rise d3">Built the Cointelegraph accelerator: 60 investments across four cohorts, $125M in follow-on funding. Techstars All-Star Mentor.</p>
  </div>
</header>
<main>
  <section><div class="sh"><h2 class="serif">Find me</h2></div>{links_html}<figure class="stage"><img src="img/kyle-cis.webp" width="600" height="480" alt="Kyle White speaking on a panel at the Crypto Invest Summit" loading="lazy" decoding="async"><figcaption>On the panel at the Crypto Invest Summit.</figcaption></figure></section>
  <section class="vault" id="vault">
    <div class="vk"><h2 class="vt serif"><small>EREDO &times; SECONDO</small>The Vault</h2><p class="big" aria-label="up to 79 percent off">79<sup>%</sup></p></div>
    <p class="vsub">Zegna, Brioni, Tod&rsquo;s, Missoni. Real Italian houses at up to 79% off, every price checked {e(VERIFIED)}.</p>
    <input class="fx" type="radio" name="vf" id="f-all" checked><input class="fx" type="radio" name="vf" id="f-eredo"><input class="fx" type="radio" name="vf" id="f-secondo">
    <div class="chips" role="group" aria-label="Filter"><label for="f-all">All<span>{len(deals)}</span></label><label for="f-eredo">Eredo<span>{houses_n['EREDO']}</span></label><label for="f-secondo">Secondo<span>{houses_n['SECONDO']}</span></label></div>
    <div class="rail">{deals_html}</div>
    <p class="swipe">Swipe &rarr;</p>
    {house_html}
  </section>
  <section class="uni">
    <div class="sh"><h2 class="serif">The Uniform</h2><span class="cap">{len(picks)} pieces</span></div>
    <p class="ulede">What I actually wear, week in, week out. Cashmere, merino, good leather. Mostly Italian.</p>
    <div class="uwrap">{feat_html}<div class="grid">{picks_html}</div></div>
  </section>
</main>
<footer>
  <p class="sig">Grazie for stopping by.</p>
  <p>Some links on this page are affiliate links. If you buy through them I may earn a commission, at no extra cost to you. Prices as listed by each store on Oct 24, 2026.</p>
</footer>
</body>
</html>
'''
open(os.path.join(D, 'index.html'), 'w').write(page)
print('built', len(page), 'bytes;', len(ticker), 'ticker items;', len(picks), 'picks')
