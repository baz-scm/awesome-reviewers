---
title: Deterministic Config Resolution
description: Ensure configuration-derived behavior (URLs, enabled/disabled state,
  selected targets, runtime environment) is resolved deterministically from a single
  source of truth, then reused—never re-computed with duplicated or drifting logic.
repository: cline/cline#v27
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70892
---

Ensure configuration-derived behavior (URLs, enabled/disabled state, selected targets, runtime environment) is resolved deterministically from a single source of truth, then reused—never re-computed with duplicated or drifting logic.

Apply these rules:
- Centralize resolution logic in shared helpers (e.g., config parsing, provider env-key handling, backend→environment mapping). Don’t keep independent “copies” of SDK/provider rules.
- Resolve provider/backend/environment values once per supported lifecycle boundary (commonly at startup). Pass the resolved value to dependent code paths (UI/webview/actions) instead of re-reading provider settings on every refresh.
- Make precedence explicit and testable: implement the correct priority between CLI flags, env vars, and config files; treat “unset” differently from an explicit negation/default.
- In tests, control the environment: clear/provide proxy/env vars so dispatchers and network behavior are stable.

Example (CLI flag vs env precedence with negatable flags):
```ts
const useMouse =
  (authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse
    : undefined) ??
  (program.getOptionValueSource("mouse") === "cli"
    ? program.opts().mouse
    : undefined) ??
  (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

Example (resolve once, build derived links from the exact resolved base):
```ts
const apiBase = await resolveBackendBaseUrlOnce();
const appBase = resolveAppBaseUrlFromBackend(apiBase); // shared helper
return appBase ? buildPrivacySettingsUrl(appBase) : undefined; // don’t open mismatched env links
```