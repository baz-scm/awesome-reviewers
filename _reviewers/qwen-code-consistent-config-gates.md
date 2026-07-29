---
title: Consistent Config Gates
description: When behavior is driven by config/flags (timeouts, scopes, feature gates,
  safe-mode), ensure every code path uses the same authoritative inputs and does not
  silently degrade.
repository: QwenLM/qwen-code
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 26407
---

When behavior is driven by config/flags (timeouts, scopes, feature gates, safe-mode), ensure every code path uses the same authoritative inputs and does not silently degrade.

**Standards**
1) **No hardcoded environment overrides for timing**: tool-call/polling waits must use env-aware defaults (or an explicitly justified env-aware formula), not fixed “one size fits all” timeouts.
2) **Single source of truth for gates/flags**: default parameter values must reference the current config gate accessor; avoid stale/legacy getters that can silently change semantics.
3) **Scope correctness (and honesty)**: enforcement logic and user-facing warnings must match the settings schema/docs, including trusted scopes (e.g., `SystemDefaults`).
4) **No machine-global security gates via per-workspace overrides**: if a setting is intended to be consistent across the host, either ignore workspace scope for it or provide a deployment-level env var mechanism; otherwise mixed behavior will occur.
5) **Mode parity (safe mode / special modes)**: status/reporting endpoints must use the same disablement and enforcement logic as execution paths.
6) **Schema validity per version**: fields that are dead in a given version must be removed from that version’s strict schema or explicitly reserved/documented.
7) **Avoid global mutable config side effects**: if you temporarily override module-level config (e.g., API host), restore it in a `finally` block.

**Example: env-aware timeout instead of hardcoded**
```ts
const toolCall = await rig.waitForAnyToolCall(
  ['write_file', 'edit'],
  rig.getDefaultTimeout(),
);
```

**Example: restore overridden host/config**
```ts
const prev = getGhHost();
try {
  setGhHost(window.host ?? undefined);
  // ... audit calls ...
} finally {
  setGhHost(prev);
}
```