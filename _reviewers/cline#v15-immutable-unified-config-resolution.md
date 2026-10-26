---
title: Immutable, Unified Config Resolution
description: 'Standard: Resolve configuration-derived values once (at startup or at
  the designated boundary), using a single agreed precedence + mapping function, and
  then treat the resolved result as immutable input. Propagate that resolved value
  everywhere (UI/webview/links/connectors). Avoid per-refresh re-resolution and avoid
  mutating semantic fields on objects...'
repository: cline/cline#v15
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70877
---

Standard: Resolve configuration-derived values once (at startup or at the designated boundary), using a single agreed precedence + mapping function, and then treat the resolved result as immutable input. Propagate that resolved value everywhere (UI/webview/links/connectors). Avoid per-refresh re-resolution and avoid mutating semantic fields on objects passed downstream.

Apply this when:
- Multiple paths could compute the same value (e.g., manifest vs code, provider baseUrl vs app baseUrl, remote selection rules).
- You mix CLI flags and environment variables, especially with negatable flags where framework defaults can clobber env fallbacks.
- Observers add telemetry/hooks but must not rewrite identity/semantic fields (e.g., sessionId signals “resume” vs “new”).

Actionable checklist:
1. Choose one resolution pipeline (single source of truth). Don’t duplicate “remote/appUrl/baseUrl/enablement” logic in different layers.
2. Resolve once: store the resolved config (e.g., ctx/appBaseUrl) and return it directly later.
3. Make precedence explicit: when a value can come from CLI or env, detect whether CLI explicitly set it; otherwise fall back to env.
4. Don’t mutate bootstrap truth: when passing configs to core, only add orthogonal properties (hooks/telemetry wiring). Preserve identity/semantic fields from the original input.

Example pattern (TypeScript):
```ts
// 1) Resolve once at startup
function resolveAppBaseUrl(resolvedBackendBaseUrl?: string): string | undefined {
  // map backend -> environment/app URL (single shared helper)
  return resolveClineAppBaseUrl(resolvedBackendBaseUrl);
}

const appBaseUrl = resolveAppBaseUrl(backendBaseUrlResolvedOnce);

// 2) Later calls just use the resolved value
function getClIneAppBaseUrlFromConfig(cfg: { appBaseUrl?: string }) {
  return cfg.appBaseUrl; // no re-resolution
}

// 3) Explicit CLI/env precedence (negatable flags)
function resolveUseMouse(opts: { mouse?: boolean }, src: { mouseValueSource?: 'cli'|'env'|'default' }, env: any) {
  if (src.mouseValueSource === 'cli') return opts.mouse;
  return env.CLINE_NO_MOUSE !== '1' && env.CLINE_MOUSE !== '0';
}

// 4) Avoid mutating semantic identity fields when configuring core
const coreInput = {
  ...originalCoreInput,
  // ONLY attach orthogonal config (e.g., hooks/telemetry)
  telemetry: originalCoreInput.telemetry ?? telemetryFromOptions,
};
// Do not change originalCoreInput.sessionId unless the caller explicitly set it.
```