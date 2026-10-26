---
title: Consistent configuration resolution
description: Ensure derived configuration (URLs, targets, auth/keys, skip/onboarding
  decisions) is computed from a single source of truth, at the correct lifecycle boundary,
  and with isolated config in tests.
repository: cline/cline#v20
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70886
---

Ensure derived configuration (URLs, targets, auth/keys, skip/onboarding decisions) is computed from a single source of truth, at the correct lifecycle boundary, and with isolated config in tests.

Apply this as a coding standard:
1) Use shared resolution helpers for derived config
- If you build a link/target that depends on environment/provider settings, derive it via the same helper used by the underlying runtime/backend resolution.
- Don’t duplicate mapping logic (e.g., “backend baseUrl vs app baseUrl”) in UI/webview/sidecars.

2) Resolve once per supported lifecycle, then pass the resolved value downstream
- If the app/backend/environment cannot change after startup, compute the resolved value once at startup and reuse it (avoid re-resolving from potentially different provider snapshots during account refresh).

3) Unify rule sets across producer/consumer paths
- If the UI shows a repo/remote and the code later pushes to a remote, both must follow the same remote-selection rule (don’t let manifest and push code diverge).

4) Centralize precedence/merge behavior for settings and auth
- Ensure merge logic prevents stale credentials/tokens from silently winning when new user input (e.g., a pasted API key) is provided.

5) Tests/smoke: isolate env/config paths and stub safely
- Run smoke tests and configuration-path tests in a temp HOME/data dir.
- Set the same discovery/config env vars your code reads.
- Stub env vars and restore them without breaking previously-unset state.

Example pattern (resolve once, pass down):
```ts
// Startup
const appBaseUrl = resolveClineAppBaseUrl(resolvedApiBaseUrl);
ctx.clineAppBaseUrl = appBaseUrl;

// Later (per account refresh/webview request)
function get_cline_app_base_url() {
  return ctx.clineAppBaseUrl; // no re-resolution here
}
```

This standard prevents “mismatch” bugs (staging vs prod links, UI showing one remote while pushing to another), avoids stale-precedence issues for auth, and keeps CI/build smoke runs from accidentally using or mutating real user configuration.