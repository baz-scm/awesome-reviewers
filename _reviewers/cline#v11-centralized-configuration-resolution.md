---
title: Centralized Configuration Resolution
description: Adopt a single, shared source of truth for derived configuration values,
  and apply explicit precedence rules (CLI > env > stored settings). Resolve “derived”
  values once at the correct lifecycle boundary when switching is unsupported, and
  never duplicate parsing/resolution logic across UI/runtime.
repository: cline/cline#v11
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70871
---

Adopt a single, shared source of truth for derived configuration values, and apply explicit precedence rules (CLI > env > stored settings). Resolve “derived” values once at the correct lifecycle boundary when switching is unsupported, and never duplicate parsing/resolution logic across UI/runtime.

Practical rules:
- Reuse shared helpers/parsers for config mapping and semantics (e.g., base URL mapping, frontmatter enabled/disabled). If two components must agree, they must call the same function.
- Use shared “usability”/eligibility checks for gating UI behavior vs runtime behavior (e.g., treat env/credential-chain as valid even if no key is saved).
- Make precedence explicit. When the framework can silently default values (e.g., negatable CLI flags), resolve based on the option’s value source, not the raw option value.
- Resolve once at startup (and pass into later calls) when environment/backend switching is not supported; avoid re-resolving per refresh/account update.
- Ensure overrides are deterministic: when a higher-priority setting (like a pasted API key) must win, clear or overwrite any lower-priority auth material rather than merging stale state.

Example: explicit precedence for a negatable flag (CLI vs env fallback)
```ts
const useMouse =
  authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse // honors --no-mouse
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
```

Example: resolve once at startup and return a stable derived value
```ts
// startup
ctx.cLineAppBaseUrl = resolveClineAppBaseUrl(resolvedBackendBaseUrl);

// later (webview request)
export function get_cline_app_base_url() {
  return ctx.cLineAppBaseUrl; // no re-resolution per refresh
}
```

Example: remove duplicated config semantics by delegating to a shared parser
```ts
// instead of local frontmatter rules, call the SDK/core helper
const disabled = isFrontmatterDisabled(parsedFrontmatterData);
```