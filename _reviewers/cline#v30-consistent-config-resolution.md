---
title: Consistent Config Resolution
description: When behavior, UI, and derived links/selections depend on configuration
  (env vars, provider settings, CLI flags, manifest defaults), resolve it consistently
  using a single source of truth, and reuse the resolved value.
repository: cline/cline#v30
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70894
---

When behavior, UI, and derived links/selections depend on configuration (env vars, provider settings, CLI flags, manifest defaults), resolve it consistently using a single source of truth, and reuse the resolved value.

Apply these rules:
1) Resolve once, then reuse
- Resolve derived values (e.g., app/privacy base URLs, selected repo/remote, default model id) once at startup/session creation from the environment/provider resolution.
- Avoid re-resolving based on account refresh when the system does not support changing the backend/environment mid-session.

2) Use shared mapping/helpers for derived values
- If you need a UI link or action target based on a backend/API resolution, build it from the same resolved backend value via a dedicated mapping helper.
- If a backend/environment has no declared mapping (proxy/self-hosted/unknown), prefer hiding/disabling actions over opening a different environment.

3) Ensure selection logic matches actual execution
- Do not let “displayed choice” and “executed target” use different selection rules (e.g., remote selection fallback differences).

4) Make precedence explicit (CLI flags vs env vs defaults)
- When combining CLI options and env fallbacks, explicitly determine which source wins.
- For negatable flags (e.g., `--no-x`), don’t rely on raw option values because framework defaults may clobber env.

Example (flag/env precedence for negatable flags):
```ts
const useMouse =
  authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
```

Example (derive UI links from resolved backend mapping):
```ts
// 1) Resolve backend base URL once (including staging overrides)
const apiBaseUrl = resolveAccountApiBaseUrl(/* ... */);
// 2) Map to the correct app/privacy base URL for that backend
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl);
// 3) If unmapped/unknown, hide instead of linking elsewhere
const privacyUrl = appBaseUrl ? buildPrivacyUrl(appBaseUrl) : undefined;
```

Outcome: fewer “mismatch” bugs where the UI shows one environment/target while the code actually calls another, and fewer surprises when env fallbacks are silently overridden by framework defaults.