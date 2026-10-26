---
title: Single Source Config Resolution
description: 'When deriving behavior from env/provider/config/CLI, treat config resolution
  as a single source of truth: use shared helpers, resolve once, and make precedence
  explicit.'
repository: cline/cline#v26
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70893
---

When deriving behavior from env/provider/config/CLI, treat config resolution as a single source of truth: use shared helpers, resolve once, and make precedence explicit.

Apply this rule:
- Don’t duplicate resolution logic across components. If multiple places need the same decision (URL mapping, enabled/disabled semantics, “is this a real API key?”, default model selection), call the same shared helper/parser instead of re-implementing.
- Resolve provider/env-derived values once during startup (or the sidecar/context initialization), then pass the resolved value through to later flows. Avoid re-resolving differently during account refreshes or per-request lifecycles.
- Define precedence and verify it with tests—especially when using negatable CLI flags (where default values can overwrite env fallbacks). Prefer “value source” detection (CLI vs env) over reading raw option values.
- Unify “what you display” vs “what you actually do”: ensure any computed remote/repo/URL used for UI or previews is derived by the exact same rules as the actual operation.

Example pattern (precedence-safe flag handling + resolve-once):
```ts
// Resolve once at startup
const appBaseUrl = resolveClineAppBaseUrl(resolvedApiBaseUrl);
ctx.clineAppBaseUrl = appBaseUrl; // pass through to webview/actions

// Precedence-safe CLI/env for negatable flags
const mouse = (cmd.getOptionValueSource('mouse') === 'cli')
  ? cmd.opts().mouse
  : process.env.CLINE_NO_MOUSE !== '1' && process.env.CLINE_MOUSE !== '0';
```

If you see any mismatch bugs (wrong environment links, different UI vs push targets, onboarding skipping differing from runtime behavior), the standard is: align both sides to the shared resolver and re-run with precedence tests.