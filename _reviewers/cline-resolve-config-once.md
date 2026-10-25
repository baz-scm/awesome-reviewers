---
title: Resolve config once
description: When behavior depends on provider/env configuration (URLs, feature links,
  capability gating), derive the *effective* configuration once using shared helpers,
  then pass the resolved values through—don’t recompute them during refresh/account
  cycles. Also, make configuration precedence explicit and test it (CLI flags vs env
  vs defaults), especially for...
repository: CLINE/cline
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70839
---

When behavior depends on provider/env configuration (URLs, feature links, capability gating), derive the *effective* configuration once using shared helpers, then pass the resolved values through—don’t recompute them during refresh/account cycles. Also, make configuration precedence explicit and test it (CLI flags vs env vs defaults), especially for negatable/boolean flags that may default to `true`.

Practical rules:
- Resolve “backend/app URL/base URL” (or equivalent effective config) once during process/sidecar startup from the existing environment resolution, and reuse that exact value to build links/actions.
- Centralize mapping logic in shared helpers; UI/webview/sidecar should consume the resolved value instead of re-reading provider settings on every refresh.
- For CLI/env precedence, prefer option “value source” (or an equivalent mechanism) over raw option values when defaults exist; otherwise env fallbacks can be silently overridden.
- For UI gating (e.g., onboarding/link visibility), reuse the same provider capability/key detection logic as the runtime.
- In tests/build smoke scripts, isolate config by using a temp HOME and explicit discovery/data paths so you don’t interact with a developer’s real running services.

Example (pattern):
```ts
// Startup: resolve once
const apiBaseUrl = resolveBackendBaseUrlOnceFromEnvAndProvider();
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // may be undefined

// Later (refresh/UI actions): reuse resolved value, don’t recompute
export function getPrivacySettingsUrl() {
  return appBaseUrl ? buildPrivacySettingsUrl(appBaseUrl) : undefined;
}

// CLI precedence guardrail
const noMouseProvidedByCli = cli.getOptionValueSource('mouse') === 'cli';
const mouse = noMouseProvidedByCli ? cli.opts().mouse : undefined;
const useMouse = mouse !== undefined ? mouse : envFallback();
```

Expected outcome: fewer environment mismatches (staging vs prod links), no drift between runtime/UI behavior, and reliable env fallback when users override via CLI.