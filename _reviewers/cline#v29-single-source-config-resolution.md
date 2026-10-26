---
title: Single-source config resolution
description: All configuration-derived decisions (URLs, feature-flag effects, parsing/enabled
  logic, provider key usability, remote/push targets, etc.) must come from one canonical
  resolver and be resolved exactly once at the appropriate lifecycle boundary, then
  passed to downstream consumers.
repository: cline/cline#v29
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70893
---

All configuration-derived decisions (URLs, feature-flag effects, parsing/enabled logic, provider key usability, remote/push targets, etc.) must come from one canonical resolver and be resolved exactly once at the appropriate lifecycle boundary, then passed to downstream consumers.

Apply:
- Use shared helpers/parsers/mappers (e.g., the SDK or runtime logic) instead of maintaining local copies.
- Resolve once (startup or at command entry), store the resolved value (e.g., `ctx.*`), and reuse it across UI/webview/account refresh cycles.
- Make precedence explicit when combining CLI flags and env vars—especially for negatable/tri-state flags—so defaults don’t overwrite env.
- Ensure any “display” computation (manifest/UI) uses the same resolved identity as the “action” computation (push/behavior).

Example pattern:
```ts
// Resolve once at entry/startup
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // canonical helper
ctx.clineAppBaseUrl = appBaseUrl; // reuse everywhere

// Later: just pass through, don’t recompute from provider/account again
webview.send({ clineAppBaseUrl: ctx.clineAppBaseUrl });
```

For CLI vs env precedence:
```ts
const useMouse = opts.mouseProvidedFrom === 'cli'
  ? opts.mouse // only trust CLI when explicitly provided
  : (process.env.CLINE_NO_MOUSE !== '1' && process.env.CLINE_MOUSE !== '0');
```