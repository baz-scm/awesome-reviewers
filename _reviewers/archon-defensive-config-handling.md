---
title: Defensive config handling
description: 'Configuration should be treated as untrusted input: validate and normalize
  it, ignore unknown/invalid fields, and ensure user misconfiguration can’t crash
  initialization or produce misleading warnings. Also gate checks by what’s actually
  configured and implement a clear precedence order (env → explicit config → user
  paths → canonical defaults → PATH lookup)...'
repository: coleam00/Archon
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 21089
---

Configuration should be treated as untrusted input: validate and normalize it, ignore unknown/invalid fields, and ensure user misconfiguration can’t crash initialization or produce misleading warnings. Also gate checks by what’s actually configured and implement a clear precedence order (env → explicit config → user paths → canonical defaults → PATH lookup) with platform-correct behavior.

Apply it like this:
- Parse YAML/env into typed config by checking `typeof` and only assigning known fields.
- For numeric settings, enforce constraints (e.g., finite and positive), normalize (e.g., truncate fractional seconds/ms), and cover invalid cases with regression tests.
- Never throw during provider/provider-discovery/config parsing; drop invalid fields instead.
- When performing environment-dependent checks, only warn when the relevant credentials/config are expected to exist; if an alternate forge is configured and GitHub token is absent, skip the GitHub-specific warning.
- When resolving external binaries, follow a documented precedence chain starting with explicit overrides, then fall back safely; ensure OS-specific lookup (e.g., Windows `where` resolving shims) is correct.

Example pattern (parser + guard):
```ts
export function parseTimeouts(raw: Record<string, unknown>) {
  const out: { firstEventTimeoutMs?: number; processTimeoutMs?: number } = {};

  const toFinitePositiveMs = (v: unknown) =>
    typeof v === 'number' && Number.isFinite(v) && v > 0 ? Math.trunc(v) : undefined;

  const first = toFinitePositiveMs(raw.firstEventTimeoutMs);
  if (first !== undefined) out.firstEventTimeoutMs = first;

  const proc = toFinitePositiveMs(raw.processTimeoutMs);
  if (proc !== undefined) out.processTimeoutMs = proc;

  return out;
}

function shouldCheckGhAuth() {
  const hasGhToken = !!(process.env.GH_TOKEN || process.env.GITHUB_TOKEN);
  const hasOtherForge = !!(process.env.GITEA_URL || process.env.GITLAB_URL);
  return hasGhToken || !hasOtherForge; // skip GH warning for non-GH-only setups
}
```