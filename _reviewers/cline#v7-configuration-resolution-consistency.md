---
title: Configuration Resolution Consistency
description: When configuration is derived from multiple sources (env vars, CLI flags,
  provider settings, manifest rules, endpoints), resolve it once from an authoritative
  source, keep a single derived value/contract across modules, and make precedence
  rules explicit.
repository: cline/cline#v7
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70865
---

When configuration is derived from multiple sources (env vars, CLI flags, provider settings, manifest rules, endpoints), resolve it once from an authoritative source, keep a single derived value/contract across modules, and make precedence rules explicit.

Apply:
- **Single source of truth for derived values:** If the backend/provider determines an app URL or other derived setting, compute it once (via a shared helper/contract) and pass that exact value through; don’t rebuild links/behavior from a different field.
- **Stable lifecycle:** If the app/account backend/environment cannot change after startup, resolve provider/environment overrides once at startup and reuse them (avoid recomputing on refresh loops).
- **Explicit precedence:** Implement a clear order like **CLI (when explicitly provided) > env > derived defaults**. Watch for negatable CLI flags (Commander defaults can clobber env) and determine whether the value came from CLI vs default.
- **No duplicated config state:** Avoid storing a second flag that mirrors host readiness/metadata; read it from the shared provider contract instead.
- **Isolate config for tests/smoke:** For env-dependent code, run in a temp/isolated HOME/data directory (and isolate discovery paths/ports) so developer machine state can’t affect results.

Example (precedence-safe CLI/env resolution):
```ts
const mouse =
  authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse // explicit flag only
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0"; // env fallback
```

Example (avoid duplicated derived config):
- Don’t add a second “providerConfigured” boolean to session config if the host already provides it via the shared provider contract; consume `apiKeyOptional` / provider metadata from the existing facts payload instead.