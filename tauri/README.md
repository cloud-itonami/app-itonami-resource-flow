# Resource Flow — Tauri v3 host (blocked: needs a release build)

Packages `../web/dist` as a Tauri 3.0.0-alpha.6 (Wry) app with the pinned canonical consent broker and a
descriptor that declares no external operation (CSP `connect-src 'self'`, no `'unsafe-eval'`).

**Blocked.** The committed `web/dist` is a shadow-cljs *development* build. Its loader runs every namespace
through `goog.globalEval`, which needs `script-src 'unsafe-eval'`. This host does not allow that, so in a
browser (and in the WebView) every namespace fails with an EvalError and `#app` stays empty. Allowing
`'unsafe-eval'` would defeat the point of deriving the CSP from the descriptor, so it is not done.

To unblock: produce a release (advanced-compiled) build of the `:app` target into `web/dist`, then
`npm run build` and re-check that the page renders with no CSP violation. That needs the cljs toolchain and is
a separate decision (see AGENTS.md on JVM use). Until then this branch must not be merged as a working app.

Everything else follows the same pattern as the other Tier 1 hosts: `vendor/` is a pinned copy of the canonical
`kotoba-client-runtime.js` and consent CSS (`vendor/PINS.json`; the build fails on drift), `npm test` runs the
node tests, and `cd src-tauri && cargo check --locked` needs `npm run build` first.
