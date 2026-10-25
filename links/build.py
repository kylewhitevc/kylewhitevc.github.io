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


market = json.load(open(os.path.join(D, 'data/market.json')))


def fmt_px(v):
    v = float(v)
    if v >= 1000: return f"${v:,.0f}"
    if v >= 1: return f"${v:,.2f}"
    return f"${v:.4f}"


def fmt_chg(c):
    c = float(c)
    return ('up' if c >= 0 else 'dn'), f"{'+' if c >= 0 else '−'}{abs(c):.2f}%"


def tick_seq():
    """About 70% market, 30% clothing: spread the deals evenly through the coins."""
    coins = market['coins']
    deals_t = sorted(ticker, key=lambda t: -int(t['pct']))[:max(1, round(len(coins) * 3 / 7))]
    seq, n, k = [], len(coins) + len(deals_t), 0
    for i in range(n):
        if k < len(deals_t) and (i + 1) * len(deals_t) // n > k:
            seq.append(('d', deals_t[k])); k += 1
        else:
            seq.append(('c', coins[i - k]))
    return seq


_rsrc = open(os.path.join(D, 'links.js')).read()
REF = json.loads(_rsrc[_rsrc.index('{', _rsrc.index('KW_REF')):].rstrip().rstrip(';'))
def ref_href(broker):
    b = REF['brokers'][broker]
    return b.get('ref') or b['url']
def coin_broker(cid):
    return REF.get('coins', {}).get(cid, REF['default'])

def tick_items(hidden=False):
    out = []
    attrs = ' tabindex="-1" aria-hidden="true"' if hidden else ''
    for kind, t in tick_seq():
        if kind == 'c':
            cls, txt = fmt_chg(t['chg'])
            out.append(
                f'<a class="tk mk" data-cg="{e(t["id"])}" data-ref="{e(coin_broker(t["id"]))}" href="{e(ref_href(coin_broker(t["id"])))}" target="_blank" rel="sponsored noopener" title="Buy {e(t["sym"])} on {e(REF["brokers"][coin_broker(t["id"])]["name"])}"{attrs}>'
                f'<b>{e(t["sym"])}</b><span class="pr">{fmt_px(t["usd"])}</span><span class="chg {cls}">{txt}</span></a>')
        else:
            out.append(
                f'<a class="tk" href="{e(t["url"])}" target="_blank" rel="sponsored noopener"{attrs}>'
                f'<b>{e(t["house"])}</b><span class="m">{e(t["maker"])}</span>'
                f'<span class="pc">{e(t["piece"])}</span><span class="pr">{money(t["price"])}</span>'
                f'<span class="off">&minus;{int(t["pct"])}%</span></a>')
    return ''.join(out)


ICON = {'linkedin': '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.79-1.7-2.79-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/>', 'x': '<path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.77zm-1.08 16.2h1.7L7.4 4.73H5.58z"/>', 'instagram': '<path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM12 2.5c-2.6 0-2.9 0-3.9.06-3.5.16-5.4 2.1-5.6 5.6C2.5 9.1 2.5 9.4 2.5 12s0 2.9.06 3.9c.16 3.5 2.1 5.4 5.6 5.6 1 .05 1.3.06 3.9.06s2.9 0 3.9-.06c3.5-.16 5.4-2.1 5.6-5.6.05-1 .06-1.3.06-3.9s0-2.9-.06-3.9c-.16-3.5-2.1-5.4-5.6-5.6-1-.05-1.3-.06-3.9-.06zm0 1.7c2.55 0 2.85 0 3.86.06 2.6.12 3.8 1.35 3.92 3.92.05 1 .06 1.3.06 3.86s0 2.85-.06 3.86c-.12 2.56-1.32 3.8-3.92 3.92-1 .05-1.3.06-3.86.06s-2.85 0-3.86-.06c-2.6-.12-3.8-1.36-3.92-3.92C4.2 14.85 4.2 14.55 4.2 12s0-2.85.06-3.86C4.38 5.56 5.6 4.32 8.14 4.2 9.15 4.2 9.45 4.2 12 4.2z"/>', 'site': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.95a15.6 15.6 0 0 0-1.38-3.56A8.03 8.03 0 0 1 18.9 8zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14a8.2 8.2 0 0 1 0-4h3.38a16.5 16.5 0 0 0 0 4zm.84 2h2.95c.32 1.25.78 2.45 1.38 3.56A8 8 0 0 1 5.1 16zm2.95-8H5.1a8 8 0 0 1 4.33-3.56C8.83 5.55 8.37 6.75 8.05 8zM12 19.96A14 14 0 0 1 10.09 16h3.82A14 14 0 0 1 12 19.96zM14.34 14H9.66a14.7 14.7 0 0 1 0-4h4.68a14.7 14.7 0 0 1 0 4zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56zM16.36 14a16.5 16.5 0 0 0 0-4h3.38a8.2 8.2 0 0 1 0 4z"/>', 'cointelegraph': '<path d="M4 4h16v2H4zm0 4h10v2H4zm0 4h16v2H4zm0 4h10v2H4z"/>', 'press': '<path d="M4 4h13v14a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2zm2 2v3h9V6zm0 5v2h9v-2zm0 4v2h6v-2zm13-7h2v10a2 2 0 0 1-2 2z"/>'}
links_html = ''.join(
    f'''<a class="row" href="{e(l['url'])}" target="_blank" rel="noopener">
      <svg class="ic" viewBox="0 0 24 24" aria-hidden="true">{ICON.get(l['id'],'')}</svg><span class="rl">{e(l['label'])}</span><span class="rs">{e(l['sub'])}</span><span class="ar" aria-hidden="true">&rarr;</span></a>'''
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
GROUP = {'Tailoring':'tailoring','Shirting':'tailoring','Knitwear':'knitwear','Shoes':'shoes'}
UG = [('all','All'),('tailoring','Tailoring'),('knitwear','Knitwear'),('shoes','Shoes'),('accessories','Accessories')]
def grp(r): return GROUP.get(r['category'],'accessories')
ug_n = {k: (len(picks) if k=='all' else sum(1 for r in picks if grp(r)==k)) for k,_ in UG}
picks_html = ''.join(
    f"""<a class="pick g-{grp(r)}{' p1' if i==1 else ''}" href="{href(r)}" target="_blank" rel="sponsored noopener">
      <span class="ph"><img src="img/{e(r['id'])}.webp" width="600" height="750" alt="{e(r['brand'])} {e(r['name'])}" loading="lazy" decoding="async"><span class="no">N&deg;{i:02d}</span></span>
      <span class="pc">{e(r['category'])}</span><span class="pb">{e(r['brand'])}</span><span class="pn">{e(r['name'])}</span>
      <span class="pf"><span class="pp">{money(r['price'])}</span><span class="po">{e(origin(r['made_in']))}</span></span></a>"""
    for i, r in enumerate(picks, 1))
ug_inputs = ''.join(f'<input class="fx" type="radio" name="uf" id="u-{k}"{" checked" if k=="all" else ""}>' for k,_ in UG)
ug_chips = ''.join(f'<label for="u-{k}">{n}<span>{ug_n[k]}</span></label>' for k,n in UG if ug_n[k])
UCSS = ''.join(f'#u-{k}:checked~.chips [for=u-{k}]{{background:var(--brass);color:#0e0b09;border-color:var(--brass)}}' for k,_ in UG) + \
  ''.join(f'#u-{k}:checked~.uwrap .pick:not(.g-{k}){{display:none}}' for k,_ in UG if k!='all') + \
  '.uni .chips{flex-wrap:wrap}#u-all:checked~.uwrap .p1{display:none}' + \
  ''.join(f'#u-{k}:checked~.uwrap .feat' for k,_ in UG if k!='all').replace('.feat#','.feat,#') + '{display:none}' + \
  '@media (min-width:760px){' + ''.join(f'#u-{k}:checked~.uwrap' for k,_ in UG if k!='all').replace('.uwrap#','.uwrap,#') + '{display:block}' + ''.join(f'#u-{k}:checked~.uwrap .grid' for k,_ in UG if k!='all').replace('.grid#','.grid,#') + '{grid-template-columns:repeat(4,1fr)}}'


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
.track{display:flex;width:max-content;animation:run 95s linear infinite}
.ticker:hover .track,.ticker:focus-within .track{animation-play-state:paused}
.tk{display:flex;align-items:center;gap:8px;height:38px;padding:0 22px;white-space:nowrap;font-size:12.5px;color:var(--ink);border-right:1px solid var(--line)}
.tk b{font-weight:600;letter-spacing:.2em;font-size:10.5px;color:var(--brass)}
.tk .m{color:var(--ink);font-weight:500}.tk .pc{color:var(--mute)}.tk .pr{font-variant-numeric:tabular-nums}
.tk .off{color:#0e0b09;background:var(--brass);font-weight:700;font-size:11px;padding:2px 6px;border-radius:2px}
.tk.mk b{color:var(--ink);letter-spacing:.14em}
.chg{font-size:11.5px;font-weight:600;font-variant-numeric:tabular-nums}.chg.up{color:#8fc49a}.chg.dn{color:#e08a7a}
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
.row{display:grid;grid-template-columns:34px 1fr auto;grid-template-areas:"i l a" "i s a";column-gap:12px;padding:18px 2px;border-bottom:1px solid var(--line);min-height:64px;align-items:center}
.ic{grid-area:i;width:20px;height:20px;fill:var(--brass);align-self:center}
.rl{grid-area:l;font-family:"Cormorant Garamond",Garamond,serif;font-size:25px;line-height:1.1}
.rs{grid-area:s;color:var(--mute);font-size:13px;margin-top:2px}
.ar{grid-area:a;color:var(--brass);font-size:22px;transition:transform .3s}
.row:hover .ar,.row:focus-visible .ar{transform:translateX(5px)}
/* stage */
.stage{margin:44px 0 0;border-top:1px solid var(--line);padding-top:28px}
.stage figcaption{display:block}
.stage .cap{display:block;font-size:10.5px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-top:14px}
.stage .st{display:block;font-size:34px;line-height:1.05;margin-top:6px;font-style:italic}
.stage .sl{display:block;color:var(--mute);font-size:13.5px;margin-top:8px}
.links{margin-top:40px;border-top:1px solid var(--line)}
.stage img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:cover}

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
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:64%;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;margin:14px -24px 0;padding:4px 24px 8px;scroll-padding:0 24px;scrollbar-width:none;-webkit-overflow-scrolling:touch;scroll-padding-left:24px;-webkit-mask-image:linear-gradient(90deg,#000 82%,transparent);mask-image:linear-gradient(90deg,#000 82%,transparent)}
.lsw{display:block;margin-top:6px;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}
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
/* family houses */
.fam{margin-top:72px}
.fgrid{display:grid;grid-template-columns:1fr;gap:12px;margin-top:22px}
.fh{position:relative;display:flex;flex-direction:column;padding:22px 20px 18px;border:1px solid var(--line);background:linear-gradient(140deg,#1b150f,#0f0b08);transition:border-color .3s,transform .3s}
.fh:hover{border-color:var(--brass);transform:translateY(-2px)}
.fno{position:absolute;top:16px;right:18px;font-family:"Cormorant Garamond",Garamond,serif;font-style:italic;color:var(--mute);font-size:15px}
.fk{font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass)}
.fnm{font-size:34px;line-height:1;margin-top:10px;letter-spacing:.04em}
.fl{color:var(--mute);font-size:13.5px;margin-top:10px;flex:1}
.fe{margin-top:16px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--brass2)}
@media (min-width:760px){.fgrid{grid-template-columns:repeat(3,1fr);gap:16px}.fh{min-height:210px}}
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

/* looks */
.looks{margin-top:72px}
.look{margin-top:26px;padding-top:22px;border-top:1px solid var(--line)}
.look:first-of-type{border-top:0;padding-top:4px}
.lno{font-size:10.5px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass)}
.lnm{font-size:36px;font-style:italic;font-weight:500;line-height:1;margin-top:6px}
.ll{color:var(--mute);font-size:13.5px;margin-top:8px;max-width:42ch}
.lpcs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 12px;margin-top:18px}
@media(min-width:760px){.lpcs{grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 18px}}
.lsw{display:block;margin-top:6px;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}
.lpcs::-webkit-scrollbar{display:none}
.lp{display:block;scroll-snap-align:start;min-width:0}
.lp[hidden],.lbuy li[hidden],.look[hidden]{display:none}
.lpi{display:block;aspect-ratio:4/5;background:#ece5d9;overflow:hidden}
.lpi img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.lp:hover .lpi img{transform:scale(1.05)}
.lpb{display:block;margin-top:9px;font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.lpn{display:block;font-family:"Cormorant Garamond",Garamond,serif;font-size:18px;line-height:1.1;margin-top:3px}
.lpp{display:block;margin-top:4px;font-size:13px;color:var(--ink);font-variant-numeric:tabular-nums}
.lsum{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;margin-top:18px}
.lwas{font-size:15px;color:var(--mute);font-variant-numeric:tabular-nums}
.lnow{font-family:"Cormorant Garamond",Garamond,serif;font-size:34px;line-height:1;color:var(--ink);font-weight:500;font-variant-numeric:lining-nums}
.lsave{flex-basis:100%;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--brass2);font-weight:700}
.lpp s{color:var(--mute);font-size:11.5px;margin-left:4px}
.lbuy{margin-top:12px}
.lbuy summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:54px;padding:0 18px;background:var(--brass);color:#0e0b09;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;cursor:pointer;-webkit-tap-highlight-color:transparent}
.lbuy summary::-webkit-details-marker{display:none}
.lbuy summary b{font-size:16px;letter-spacing:.02em;font-variant-numeric:tabular-nums}
.lbuy[open] summary{background:var(--brass2)}
.lbuy ol{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-top:0}
.lbuy li+li{border-top:1px solid var(--line)}
.lbuy li a{display:grid;grid-template-columns:1fr auto;gap:3px 14px;align-items:baseline;padding:13px 18px;min-height:56px}
.rb{font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.rp{font-size:14px;font-variant-numeric:tabular-nums;text-align:right}
.rn{font-family:"Cormorant Garamond",Garamond,serif;font-size:18px;line-height:1.1}
.rs{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--brass2);text-align:right}
.fimg{display:block;margin:-22px -20px 16px;aspect-ratio:4/3;overflow:hidden;background:#ece5d9}
.fimg img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.fh:hover .fimg img{transform:scale(1.04)}
#family-strip{max-width:1080px;margin:0 auto;color:var(--mute)}
@media (min-width:760px){
 .lpcs{grid-auto-flow:row;grid-template-columns:repeat(5,1fr);overflow:visible;margin:18px 0 0;padding:0;-webkit-mask-image:none;mask-image:none}
 .lsw{display:none}
 .lbuy, .lnm{font-size:48px}
}

/* stat band */
.stats{display:grid;grid-template-columns:1fr 1fr;margin-top:40px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sb{display:flex;flex-direction:column;align-items:flex-start;padding:20px 4px 18px 0}
.sb:nth-child(odd){padding-right:14px}
.sb:nth-child(even){padding-left:18px;border-left:1px solid var(--line)}
.sb:nth-child(n+3){border-top:1px solid var(--line)}
.sn{font-size:42px;line-height:.9;font-weight:500;color:var(--brass2);letter-spacing:-.01em;font-variant-numeric:lining-nums}
.sl2{margin-top:9px;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}
.stats+.links{margin-top:0;border-top:0}
@media (min-width:760px){
 .stats{grid-template-columns:repeat(4,1fr)}
 .sb{padding:26px 0 24px 24px!important;border-left:1px solid var(--line);border-top:0!important}
 .sb:first-child{border-left:0;padding-left:0!important}
 .sn{font-size:64px}
}

/* broker CTA strip */
.cta{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;max-width:1080px;margin:0 auto;padding:12px 24px 10px;border-bottom:1px solid var(--line)}
.ctl{font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-right:4px}
.ctb{display:inline-flex;align-items:baseline;gap:7px;min-height:36px;align-items:center;padding:0 14px;border:1px solid var(--line);border-radius:40px;transition:border-color .25s}
.ctb:hover{border-color:var(--brass)}
.ctb b{font-size:12.5px;font-weight:600;color:var(--ink)}
.ctb i{font-style:normal;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.ctd{flex-basis:100%;font-size:11px;color:var(--mute);margin:2px 0 0}
@media (max-width:420px){.ctb i{display:none}.ctl{flex-basis:100%}}
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
 .links{display:grid;grid-template-columns:1fr 1fr;column-gap:40px}
 .stage{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
 .stage .st{font-size:56px}
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
JS = r'''<script>
(function(){var ids=[].slice.call(document.querySelectorAll('[data-cg]')).map(function(a){return a.dataset.cg}).filter(function(v,i,a){return a.indexOf(v)===i});
function px(v){return v>=1000?'$'+Math.round(v).toLocaleString('en-US'):v>=1?'$'+v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}):'$'+v.toFixed(4)}
function go(){fetch('https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&include_24hr_change=true&ids='+ids.join(',')).then(function(r){return r.json()}).then(function(d){
document.querySelectorAll('[data-cg]').forEach(function(a){var q=d[a.dataset.cg];if(!q||q.usd==null)return;var c=q.usd_24h_change||0;
a.querySelector('.pr').textContent=px(q.usd);var s=a.querySelector('.chg');s.textContent=(c>=0?'+':'\u2212')+Math.abs(c).toFixed(2)+'%';s.className='chg '+(c>=0?'up':'dn')})}).catch(function(){})}
go();setInterval(go,60000)})();
</script>'''

_lsrc = open(os.path.join(D, 'data', 'looks.js')).read()
LK = json.loads(_lsrc[_lsrc.index('{', _lsrc.index('KW_LOOKS')):].rstrip().rstrip(';'))
def _live(k):
    p = LK['links'].get(k)
    return bool(p and p.get('live', True) and p.get('url'))
def _sums(keys):
    P = LK['links']
    now = round(sum(P[k]['price'] for k in keys))
    was = round(sum((P[k].get('was') or P[k]['price']) for k in keys))
    save = was - now
    pct = int(save * 100 // was) if was else 0
    return now, was, save, pct
def sum_html(keys):
    now, was, save, pct = _sums(keys)
    if save > 0 and pct >= 1:
        return f'<div class="lsum"><s class="lwas">{money(was)}</s><span class="lnow">{money(now)}</span><b class="lsave">Save {money(save)} ({pct}%)</b></div>'
    return f'<div class="lsum"><span class="lnow">{money(now)}</span></div>'
looks_html = ''
_n = 0
for lk in LK['looks']:
    keys = [k for k in lk['pieces'] if _live(k)]
    if len(keys) < 2:
        continue
    _n += 1
    P = LK['links']
    def _pp(k):
        w = P[k].get('was')
        return f"{money(P[k]['price'])}" + (f" <s>{money(w)}</s>" if w and w > P[k]['price'] else '')
    pcs = ''.join(f"""<a class="lp" data-k="{e(k)}" href="{e(P[k]['url'])}" target="_blank" rel="sponsored noopener"><span class="lpi"><img src="{e(P[k]['img'])}" width="600" height="750" alt="{e(P[k]['brand'])} {e(P[k]['name'])}" loading="lazy" decoding="async"></span><span class="lpb">{e(P[k]['brand'])}</span><span class="lpn">{e(P[k]['name'])}</span><span class="lpp">{_pp(k)}</span></a>""" for k in keys)
    rows = ''.join(f"""<li data-k="{e(k)}"><a href="{e(P[k]['url'])}" target="_blank" rel="sponsored noopener"><span class="rb">{e(P[k]['brand'])}</span><span class="rp">{money(P[k]['price'])}</span><span class="rn">{e(P[k]['name'])}</span><span class="rs">Shop &rarr;</span></a></li>""" for k in keys)
    looks_html += f"""<article class="look" data-look="{e(lk['id'])}">
  <h3 class="lnm serif">{e(lk['name'])}</h3><p class="ll">{e(lk.get('note',''))}</p>
  <div class="lpcs">{pcs}</div>
  {sum_html(keys)}
  <details class="lbuy" open><summary><span>Shop the full look</span><span aria-hidden="true">&darr;</span></summary><ol>{rows}</ol></details>
</article>"""
LOOKS_JS = r"""<script>
(function(){
var REMOTE='https://eredo-house-eredo.static.hf.space/looks.json';
function money(v){return '$'+Math.round(v).toLocaleString('en-US')}
function pp(p){return money(p.price)+(p.was&&p.was>p.price?' <s>'+money(p.was)+'</s>':'')}
function apply(D){
  if(!D||!D.links)return;
  document.querySelectorAll('.look').forEach(function(el){
    var n=0,now=0,was=0;
    el.querySelectorAll('.lp').forEach(function(a){
      var k=a.dataset.k,p=D.links[k],row=el.querySelector('li[data-k="'+k+'"]');
      var ok=p&&p.live!==false&&p.url&&!a.dataset.dead;
      a.hidden=!ok;if(row)row.hidden=!ok;
      if(!ok)return;
      n++;now+=+p.price||0;was+=+(p.was||p.price)||0;
      if(/^https:/.test(p.url)){a.href=p.url;if(row)row.querySelector('a').href=p.url}
      a.querySelector('.lpp').innerHTML=pp(p);if(row)row.querySelector('.rp').textContent=money(p.price);
    });
    el.hidden=n<2;
    var N=Math.round(now),W=Math.round(was),S=W-N,P=W?Math.floor(S*100/W):0,box=el.querySelector('.lsum');
    if(box)box.innerHTML=(S>0&&P>=1)?'<s class="lwas">'+money(W)+'</s><span class="lnow">'+money(N)+'</span><b class="lsave">Save '+money(S)+' ('+P+'%)</b>':'<span class="lnow">'+money(N)+'</span>';
  });
  var s=document.getElementById('looks');if(s)s.hidden=!document.querySelector('.look:not([hidden])');
}
var LOCAL=window.KW_LOOKS,CUR=LOCAL;
document.querySelectorAll('.lp img').forEach(function(i){function dead(){i.closest('.lp').dataset.dead=1;apply(CUR)}
  if(i.complete&&i.naturalWidth===0)dead();else i.addEventListener('error',dead)});
apply(LOCAL);
if(window.fetch&&LOCAL)fetch(REMOTE).then(function(r){return r.ok?r.json():null}).then(function(R){
  if(!R||typeof R.links!=='object')return;
  var byUrl={};Object.keys(R.links).forEach(function(k){var p=R.links[k];if(p&&p.url)byUrl[p.url.replace(/^https:\/\/(www\.)?/,'')]=p});
  var M={house:LOCAL.house,looks:LOCAL.looks,links:{}};
  Object.keys(LOCAL.links).forEach(function(k){var a=LOCAL.links[k],b=byUrl[a.url.replace(/^https:\/\/(www\.)?/,'')];
    M.links[k]=b?{brand:a.brand,name:a.name,img:a.img,url:a.url,price:+b.price||a.price,was:(b.was===null||b.was===undefined)?a.was:+b.was,live:b.live!==false}:a});
  CUR=M;apply(M)}).catch(function(){});
var fs=document.createElement('script');fs.src='https://eredo-house-eredo.static.hf.space/family.js';fs.async=true;
fs.onerror=function(){var v=document.createElement('script');v.src='vendor/family.js';document.body.appendChild(v)};
document.body.appendChild(fs);
})();
</script>"""
stats_html = ''.join(f'<div class="sb"><span class="sn serif">{e(x["n"])}</span><span class="sl2">{e(x["l"])}</span></div>' for x in L.get('stats',[]))
cta_html = '<div class="cta"><span class="ctl">Open an account</span>' + ''.join(f'<a class="ctb" data-ref="{e(k)}" href="{e(ref_href(k))}" target="_blank" rel="sponsored noopener"><b>{e(REF["brokers"][k]["name"])}</b><i>{e(REF["brokers"][k]["tag"])}</i></a>' for k in REF['strip']) + '<p class="ctd">I may earn a referral fee if you open an account. Not investment advice.</p></div>'
houses_live = [h for h in L['houses'] if h.get('url')]
fam_html = ''.join(f'''<a class="fh" href="{e(h['url'])}" target="_blank" rel="noopener">{('<span class="fimg"><img src="'+e(h['img'])+'" width="600" height="750" alt="'+e(h['name'])+'" loading="lazy" decoding="async"></span>') if h.get('img') else ''}<span class="fno">N&deg;{i:02d}</span><span class="fk">{e(h['kind'])}</span><span class="fnm serif">{e(h['name'])}</span><span class="fl">{e(h['line'])}</span><span class="fe">Enter &rarr;</span></a>''' for i,h in enumerate(houses_live,1))
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
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="img/icon-192.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap">
<link rel="preload" as="image" href="img/kyle-hero.webp">
<style>{CSS}{UCSS}</style>
</head>
<body>
<nav class="ticker" aria-label="Crypto prices (tap to open an account) and today's markdowns">
  <div class="track"><div style="display:flex">{tick_items()}</div><div class="dup" style="display:flex">{tick_items(True)}</div></div>
</nav>
{cta_html}
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
  <div class="stats" aria-label="Reach and track record">{stats_html}</div>
  <section class="links">{links_html}</section>
  <figure class="stage"><img src="img/kyle-cis.webp" width="720" height="720" alt="Kyle White speaking on a panel at the Crypto Invest Summit" loading="lazy" decoding="async"><figcaption><span class="cap">On stage</span><span class="st serif">Crypto Invest Summit</span><span class="sl">Panelist, Blockchain Technology Investing track.</span></figcaption></figure>
  <section class="looks" id="looks">
    <div class="sh"><h2 class="vt serif"><small>Shop the look</small>The Outfit</h2></div>
    {looks_html}
  </section>
  <section class="fam" id="houses">
    <div class="sh"><h2 class="vt serif"><small>The family</small>The Houses</h2></div>
    <p class="ulede">Each one its own shop, each with a single focus.</p>
    <div class="fgrid">{fam_html}</div>
  </section>
</main>
<footer>
  <p class="sig">Grazie for stopping by.</p>
  <p>Some links on this page are affiliate links. If you buy through them I may earn a commission, at no extra cost to you. Prices as listed by each store on Oct 25, 2026.</p>
</footer>
<div id="family-strip"></div>
<script src="data/looks.js"></script>
{LOOKS_JS}
{JS}
</body>
</html>
'''
import hashlib, re
def _v(m):
    p = os.path.join(D, m.group(1))
    h = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8] if os.path.exists(p) else ''
    return f'src="{m.group(1)}?v={h}"' if h else m.group(0)
page = re.sub(r'src="((?:img|data|vendor)/[^"?]+)"', _v, page)
page = re.sub(r'href="(img/[^"?]+)"', lambda m: 'href=' + _v(m)[4:], page)
open(os.path.join(D, 'index.html'), 'w').write(page)
print('built', len(page), 'bytes;', len(ticker), 'ticker items;', len(picks), 'picks')
