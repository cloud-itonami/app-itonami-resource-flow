# cljs release bundle built by an oracle (2026-11-17)

ORACLE evidence, not a native build. The committed `web/dist/js/main.js` is the output of a JVM
shadow-cljs release run on a mirror of the `.cljk` sources. No CI, gate, packaging or runtime path
depends on it; the Tauri host only copies the committed bundle.

- Command: `python3 oracle/cljs-release-oracle.py <work> app-itonami-resource-flow app`
  (mirrors `.cljk` -> `.cljc` and `.mjs` -> `.js` into a scratch dir, overrides every
  `io.github.kotoba-lang/*` dependency with the local worktree, runs `shadow-cljs -A:oracle release app`).
- Tools: node v26.0.0, npm 11.12.1, openjdk 21.0.1, shadow-cljs 2.28.20,
  kotoba-lang/kotoba@426ddd2a635b6714ad60a8d7852f4f802e3e54b6 (sparse `lib/`).
- Input: this repository at 7800f83522d0d62ec2c754a98b42e52488ba9533.
- Output: `[:app] Build completed. (108 files, 1 compiled, 1 warnings)`, exit 0;
  `web/dist/js/main.js` 415,658 bytes, sha256 bcd6ed70e0a40340589335c927d420d1cdb8d0d2372c12968683198d339ff342; `cljs-runtime/` (dev build) removed.
- Check: Tauri host built from it renders the page in Chromium under a CSP with no `'unsafe-eval'`;
  no EvalError. Two console errors remain and are intended: the page's fetch to
  `atproto.etzhayyim.com` is blocked because the descriptor declares no service (consent broker), and
  dynamically set inline styles are blocked by the hash-only `style-src`.
- Not shown: that this bundle behaves like the dev build with live data; that a native (Amu) build
  would produce the same code.
