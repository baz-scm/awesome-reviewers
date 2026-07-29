---
title: Collision-Safe Keys
description: When an algorithm derives a decision key (dedupe) or signal (parsed config)
  that can suppress/merge data, make that derivation collision- and normalization-safe,
  and define precedence explicitly.
repository: nousresearch/hermes-agent
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 221948
---

When an algorithm derives a decision key (dedupe) or signal (parsed config) that can suppress/merge data, make that derivation collision- and normalization-safe, and define precedence explicitly.

**Dedupe keys (avoid collision-based suppression):**
- Don’t rely on short/non-unique hashes (e.g., 32-bit) when a collision would silently drop valid items.
- Prefer a collision-resistant digest of the actual bytes (e.g., SHA-256), or use a two-phase approach: quick hash + byte-by-byte comparison as a tie-breaker.

```ts
import { createHash } from 'node:crypto'

export function imageDedupeKey(blob: Blob, data: Uint8Array): string {
  // Collision-resistant key: hash actual bytes (optionally include size)
  const digest = createHash('sha256').update(data).digest('hex')
  return `${blob.size}|${digest}`
}
```

**Parsed/merged config (normalize + deterministic precedence):**
- Normalize inputs (commonly casing) before evaluating “inherited vs system” or “user vs system.”
- Define precedence rules in one place (e.g., “if any inherited proxy spelling is set, skip all system injection”), and cover mixed-case regression tests.

```ts
function hasAnyInheritedProxy(env: Record<string, string>, family: 'http'|'https') {
  const keys = [
    `${family}_proxy`,
    `${family.toUpperCase()}_PROXY`
  ]
  return keys.some(k => (env[k] ?? '').length > 0)
}
```

**Why:** these patterns prevent subtle, hard-to-debug behavior like “silent suppression” from hash collisions and inconsistent merging from incomplete normalization/precedence handling.