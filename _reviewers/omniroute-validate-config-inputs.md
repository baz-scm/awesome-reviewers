---
title: Validate Config Inputs
description: Any configuration derived from environment variables or external config
  must be (1) wired to the correct runtime fields, (2) normalized/validated with safe
  defaults, and (3) applied with deterministic precedence.
repository: diegosouzapw/OmniRoute
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 33162
---

Any configuration derived from environment variables or external config must be (1) wired to the correct runtime fields, (2) normalized/validated with safe defaults, and (3) applied with deterministic precedence.

Practical standards:
- **Normalize env-derived values**: e.g., for hostnames, rely on URL parsing normalization but defensively normalize case.
- **Validate numeric env params**: parse with `Number.isFinite(...)` and enforce sane bounds; fall back to a documented default if invalid.
- **Avoid hardcoding runtime ports/URLs**: derive from env with a clear fallback chain.
- **Enforce config precedence deterministically**: when mixing hardcoded and DB-driven rules, define an explicit order (e.g., provider-level denylist → model-level denylist → allowlists) and ensure allowlist restoration only reintroduces keys that existed in the original request snapshot.
- **Prevent mismatched config shapes**: when config is “flattened” before reaching your class/function, assert the exact runtime fields you consume.

Example (env validation + deterministic deny/allow precedence):
```ts
// 1) Env numeric validation with fallback
const parsed = parseInt(process.env.PRICING_SYNC_INTERVAL ?? "86400", 10);
const intervalMs = Number.isFinite(parsed) && parsed > 0
  ? parsed * 1000
  : 86400 * 1000; // 24h fallback

// 2) Snapshot-based allowlist restoration
function applyFilters({ provider, model, body, snapshot, cfg }: {
  provider: string; model: string; body: Record<string, unknown>; snapshot: Record<string, unknown>; cfg: any;
}) {
  // denylist: provider
  for (const k of cfg.block ?? []) delete body[k];
  // denylist: model
  for (const k of (cfg.models?.[model]?.block ?? [])) delete body[k];
  // allowlist: provider (restore only keys that were present originally)
  for (const k of (cfg.allow ?? [])) if (k in snapshot) body[k] = snapshot[k];
  // allowlist: model (most specific wins by applying last)
  for (const k of (cfg.models?.[model]?.allow ?? [])) if (k in snapshot) body[k] = snapshot[k];
}
```

Adopt this pattern whenever config impacts runtime behavior (HTTP targets, auth payloads, request parameter shaping, sync intervals/feature flags): fail safely, default predictably, and keep behavior order explicit.