"""Gate and deploy Kyle White Links to GitHub Pages.
Usage: python3 deploy.py file [file ...]   (paths relative to links/, e.g. index.html data/looks.js)
1) Rebuilds index.html, 2) runs the looks check and a JS syntax check locally (aborts on any failure),
3) pushes checker/scripts first, then data, then index.html, so no intermediate commit on main is inconsistent."""
import base64, json, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(D)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"GATE FAILED: {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return r.stdout
run(['python3', 'build.py'])
run(['node', 'scripts/check_looks.js'])
js = '\n;\n'.join(re.findall(r'<script>(.*?)</script>', open('index.html').read(), re.S))
open('/tmp/_kw_inline.js', 'w').write(js)
run(['node', '--check', '/tmp/_kw_inline.js'])
for f in ['links.js', 'data/looks.js']:
    run(['node', '-e', f"const vm=require('vm');vm.runInNewContext(require('fs').readFileSync('{f}','utf8'),{{window:{{}}}})"])
files = sys.argv[1:] or ['index.html']
rank = lambda p: 0 if p.startswith('scripts/') else (1 if p.startswith(('data/', 'links.js', 'vendor/', 'img/')) else (3 if p == 'index.html' else 2))
for f in sorted(set(files), key=rank):
    g = subprocess.run(['apicall', 'github', 'contents_get', 'owner=kylewhitevc', 'repo=kylewhitevc.github.io', 'path=links/' + f], capture_output=True, text=True).stdout
    try: sha = json.loads(g).get('sha')
    except Exception: sha = None
    a = ['apicall', 'github', 'contents_put', 'owner=kylewhitevc', 'repo=kylewhitevc.github.io', 'path=links/' + f,
         'message=' + os.environ.get('MSG', 'Update ' + f), 'content=' + base64.b64encode(open(f, 'rb').read()).decode()]
    if sha: a.append('sha=' + sha)
    out = subprocess.run(a, capture_output=True, text=True).stdout
    print(f, 'ok' if '"content"' in out else 'FAILED ' + out[:200])
