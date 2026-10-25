---
title: Resolve config once
description: Derived configuration should be resolved exactly once using the same
  shared helpers/constants, then treated as immutable bootstrap truth. Avoid duplicating
  resolution/parsing logic across layers, and make precedence explicit so explicit
  inputs don’t get overridden silently by env/defaults/leftover state.
repository: cline/CLINE
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70839
---

Derived configuration should be resolved exactly once using the same shared helpers/constants, then treated as immutable bootstrap truth. Avoid duplicating resolution/parsing logic across layers, and make precedence explicit so explicit inputs don’t get overridden silently by env/defaults/leftover state.

Do this:
- Single source of truth: use shared resolution/parsing helpers (don’t re-implement frontmatter enablement, provider readiness, app base URL mapping, or provider env exclusions in multiple places).
- Resolve once: compute derived values at startup (or at the same resolution boundary as the rest of the context) and pass the resolved result forward instead of re-reading provider/settings on refresh.
- Explicit precedence: implement a clear order (caller-supplied/explicit flag > CLI source when provided > env fallback > default) and add tests for “all combinations”. Don’t read raw negatable defaults that can clobber env.
- No semantic mutation: observer-like code (telemetry, wrappers) may add hooks/telemetry side effects, but must not rewrite semantic fields in the config payload that downstream logic interprets.

Example patterns:
1) Resolve backend once, then build links from the resolved backend mapping:
```ts
const apiBaseUrl = resolveAccountApiBaseUrl(providerResolvedBackendBaseUrl);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // trailing slash/override safe
const privacyUrl = appBaseUrl ? getClinePrivacySettingsUrl(user.dataPrivacyPath, appBaseUrl, "cli") : undefined;
```
2) Respect CLI/env precedence for negated flags:
```ts
const mouse = (getOptionValueSource("mouse") === "cli")
  ? authCmd.opts().mouse // only if user explicitly set via CLI
  : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0"; // env fallback
```

Applying these rules prevents environment mismatch (wrong URLs), drift between SDK vs UI logic, and subtle precedence bugs that only appear in staging/overridden environments.