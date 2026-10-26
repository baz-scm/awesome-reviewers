---
title: Invariant-Based Event Logic
description: When turning asynchronous inputs (events/timers/data) into derived UI
  state or summaries, use explicit, invariant-driven state modeling and locale-safe
  output construction.
repository: cline/cline#v8
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70867
---

When turning asynchronous inputs (events/timers/data) into derived UI state or summaries, use explicit, invariant-driven state modeling and locale-safe output construction.

**Apply this standard**
1. **Model explicit states + sentinels**
   - Keep a small set of named states (e.g., `pinned`/`unpinned`, `hold tracking` vs `idle`).
   - Track “who caused it” (user vs programmatic) with a sentinel (e.g., `ourScrollTarget`) and clear arrival/release rules.
   - For timer-based behavior, define thresholds as constants and document platform-specific invariants.

2. **Define transitions as rules, not guesses**
   - Example transition rules for scroll pinning:
     - Un-pin only on true user intent (`wheel deltaY < 0`, `ArrowUp/PageUp/Home`).
     - Re-pin only when you *reach the bottom* or when your own programmatic scroll has arrived.

3. **Build human-readable summaries with locale-aware formatting**
   - Avoid hardcoded comma/space joining for translated UI strings.
   - Prefer locale-aware list formatting and ensure each “part” is a complete phrase.

**Example (locale-safe list assembly)**
```ts
const parts = [
  /* e.g., t('...files', {count}), t('...folders', {count}) */
];
if (parts.length === 0) return t('contextFallback');
const list = new Intl.ListFormat(undefined, { type: 'conjunction' }).format(parts);
return t('contextTemplate', { items: list });
```

This reduces accidental state leaks in event-driven logic and prevents translation/word-order failures in derived summaries.