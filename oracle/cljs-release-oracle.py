#!/usr/bin/env python3
"""ORACLE (not part of any native build, gate or packaging path): produce a shadow-cljs release bundle
from a Kotoba .cljk project by mirroring .cljk -> .cljc (and .mjs -> .js) into a scratch dir and
running `shadow-cljs release` on the JVM. Output is evidence, not a source of truth.

Layout it needs (the org layout the repo's deps.edn assumes):
  <work>/kotoba-lang/kotoba   sparse worktree (lib/) at a pinned revision
  <work>/cloud-itonami/<repo> the project clone, with `npm i --no-save shadow-cljs@2.28.20` done

    cljs-release-oracle.py <work> <repo> [build-id]
"""
import os, re, shutil, subprocess, sys

work, repo = os.path.abspath(sys.argv[1]), sys.argv[2]
build = sys.argv[3] if len(sys.argv) > 3 else 'app'
K = work + '/kotoba-lang/kotoba/lib'
M = work + '/mirror'
proj = f'{work}/cloud-itonami/{repo}'
shutil.rmtree(M, ignore_errors=True)
paths = []

def mirror(src, dst):
    for d, _, fs in os.walk(src):
        for f in fs:
            if f.endswith(('.cljk', '.mjs')):
                o = os.path.join(dst, os.path.relpath(d, src)); os.makedirs(o, exist_ok=True)
                new = f[:-5] + '.cljc' if f.endswith('.cljk') else f[:-4] + '.js'
                shutil.copyfile(os.path.join(d, f), os.path.join(o, new))

for lib in sorted(os.listdir(K)):
    if os.path.isdir(f'{K}/{lib}/src'):
        mirror(f'{K}/{lib}/src', f'{M}/lib/{lib}'); paths.append(f'{M}/lib/{lib}')
mirror(proj + '/src', M + '/app'); paths.append(M + '/app')
for d, _, fs in os.walk(M):
    for f in fs:
        if f.endswith('.cljc'):
            p = os.path.join(d, f); t = open(p, encoding='utf8').read()
            u = re.sub(r'\.mjs"', '.js"', t)
            if u != t: open(p, 'w', encoding='utf8').write(u)
ov = {m.group(1): m.group(2) for m in re.finditer(r'io\.github\.kotoba-lang/(\S+)\s+\{:local/root "([^"]+)"\}', open(K + '/deps.edn').read())
      if os.path.isdir(K + '/' + m.group(2))}
os.makedirs(work + '/clj-config', exist_ok=True)
open(work + '/clj-config/deps.edn', 'w').write('{:aliases {:oracle {:extra-paths [' + ' '.join('"%s"' % p for p in paths) + '] :override-deps {'
    + ' '.join(f'io.github.kotoba-lang/{k} {{:local/root "{K}/{v}"}}' for k, v in ov.items()) + '}}}}\n')
p = subprocess.run(['./node_modules/.bin/shadow-cljs', '-A:oracle', 'release', build], cwd=proj,
                   env={**os.environ, 'CLJ_CONFIG': work + '/clj-config'})
sys.exit(p.returncode)
