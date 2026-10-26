---
title: Config Precedence Rules
description: Ensure every config value (URLs/endpoints/feature flags) is resolved
  from a single source of truth with explicit precedence, so different code paths
  can’t disagree.
repository: cline/cline#v25
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70891
---

Ensure every config value (URLs/endpoints/feature flags) is resolved from a single source of truth with explicit precedence, so different code paths can’t disagree.

**Rules**
1. **Derive user-facing settings from the resolved backend/provider** using a shared helper (backend → environment/app URL). If nothing matches, hide/disable the feature instead of opening another environment.
2. **Resolve stable config once** (startup / workspace initialization) and pass the resolved value through context; don’t re-resolve it on each refresh call when the backend won’t change.
3. **Precedence is explicit:** `caller/explicit option > provider/resolved backend config > derived default`.
4. **CLI flags + env fallback:** for negatable/boolean flags, determine whether the value came from the CLI (option source), not by reading the raw boolean (Commander may default it and clobber env).
5. **Centralize “usability” checks:** if a provider may work without an API key saved on disk (via env/credential chain), use a shared `is*Usable` check rather than rejecting early.

**Example (CLI precedence for negatable flags)**
```ts
const mouse =
  authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse
    : undefined;

const useMouse =
  mouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

**Example (backend → environment mapping + resolve once)**
```ts
// at startup
const backendBaseUrl = resolveAccountApiBaseUrl(...);
const appBaseUrl = resolveClineAppBaseUrl(backendBaseUrl); // may be undefined
ctx.clineAppBaseUrl = appBaseUrl;

// later (webview action handler)
return { actionUrl: ctx.clineAppBaseUrl ? `${ctx.clineAppBaseUrl}/privacy` : undefined };
```

Applying these rules prevents environment mismatches, silent option/env override bugs, and “different subsystems made different decisions” failures.