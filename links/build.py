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

houses_html = ''.join(
    f'''<a class="house" href="{e(h['url'])}" target="_blank" rel="noopener">
      <img src="{e(h['img'])}" width="800" height="1000" alt="" loading="lazy" decoding="async">
      <span class="hn">{e(h['name'])}</span><span class="hl">{e(h['line'])}</span><span class="hc">Enter the shop &rarr;</span></a>'''
    for h in L['houses'] if h.get('url'))

picks_html = ''.join(
    f'''<a class="pick" href="{e(r['affiliate_url'].strip() or r['url'])}" target="_blank" rel="sponsored noopener">
      <span class="ph"><img src="img/{e(r['id'])}.webp" width="600" height="750" alt="{e(r['brand'])} {e(r['name'])}" loading="lazy" decoding="async"></span>
      <span class="pb">{e(r['brand'])}</span><span class="pn">{e(r['name'])}</span><span class="pp">{money(r['price'])}</span></a>'''
    for r in picks)

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
.hero img{width:100%;height:100%;object-fit:cover;object-position:50% 22%;filter:sepia(.12) saturate(.9);transform:scale(1.06);animation:settle 2.4s cubic-bezier(.2,.7,.2,1) forwards}
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
/* house */
.house{display:block;position:relative;margin-top:16px;overflow:hidden;background:#f3ebdd;color:#1a140f}
.house img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.house:hover img{transform:scale(1.03)}
.house .hn,.house .hl,.house .hc{position:absolute;left:22px;right:22px}
.house .hn{top:20px;font-family:"Cormorant Garamond",Garamond,serif;font-size:44px;letter-spacing:.32em;font-weight:500}
.house .hl{bottom:58px;font-size:15px;max-width:30ch;color:#3b3027}
.house .hc{bottom:22px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#7a5a24;font-weight:600}
/* picks */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px 14px;margin-top:18px}
.pick{display:block}
.pick:first-child{grid-column:1/-1}
.ph{display:block;overflow:hidden;background:#f2eee8;aspect-ratio:4/5}
.ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.pick:hover .ph img{transform:scale(1.04)}
.pb{display:block;margin-top:10px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.pn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:20px;line-height:1.15;margin-top:3px}
.pick:first-child .pn{font-size:26px}
.pp{display:block;color:var(--mute);font-size:13px;margin-top:2px;font-variant-numeric:tabular-nums}
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
 .grid{grid-template-columns:repeat(3,1fr);gap:34px 22px}
 .pick:first-child{grid-column:auto}.pick:first-child .pn{font-size:20px}
}
@media (prefers-reduced-motion:reduce){
 *{animation:none!important;transition:none!important}
 .rise{opacity:1;transform:none}.hero img{transform:none}
 .ticker{overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
 .track .dup{display:none}
}
"""

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
  <figure><img src="img/kyle-hero.webp" width="380" height="475" alt="Kyle White speaking on a panel at the Crypto Invest Summit" fetchpriority="high"></figure>
  <div class="intro">
    <p class="cap rise">Youngstown, Ohio</p>
    <h1 class="serif rise d2">Kyle <i>White</i></h1>
    <p class="lede serif rise d3">I build accelerators and back founders. Off the clock, it&rsquo;s Italian cashmere and good leather.</p>
    <p class="facts rise d3">Built the Cointelegraph accelerator: 60 investments across four cohorts, $125M in follow-on funding. Techstars All-Star Mentor.</p>
  </div>
</header>
<main>
  <div class="cols">
    <section><div class="sh"><h2 class="serif">Find me</h2></div>{links_html}</section>
    <section><div class="sh"><h2 class="serif">My shop</h2><span class="cap">Est. 2026</span></div>{houses_html}</section>
  </div>
  <section><div class="sh"><h2 class="serif">What I wear</h2><span class="cap">{len(picks)} pieces</span></div>
    <div class="grid">{picks_html}</div>
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
