---
title: Cache correctness rules
description: 'Use this checklist whenever you add or change caching:


  1) Define dependencies: List every input/state that can change the correctness of
  the cached value (e.g., category+storage, account+marketplace URL, connection metered-state,
  ignoreCase spelling, DOM state).'
repository: microsoft/VSCode
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 194303
---

Use this checklist whenever you add or change caching:

1) Define dependencies: List every input/state that can change the correctness of the cached value (e.g., category+storage, account+marketplace URL, connection metered-state, ignoreCase spelling, DOM state).
2) Key completeness: Ensure the cache key reflects *all* semantic dependencies. Do not “fold” key components in a way that changes result identity (e.g., ignore-case caches must not return values tied to a different original spelling/result).
3) Coupled invalidation: If you clear/refresh only part of the related state, you can create cross-product bugs. Either clear all coupled inputs together or revalidate the entire set before consuming cached results.
4) Supersede in-flight work: When context changes can happen during async operations, cancel superseded requests/validations so late completions can’t repopulate caches with stale verdicts.
5) TTL/negative-cache discipline: For time-based caches (including “not found”/negative caches), choose a TTL that matches expected propagation time; document whether you rely on periodic refresh vs require a force-refresh mechanism.
6) Virtual-structure safety: If caching references to DOM/layout/container nodes, ensure the cached reference is safe for the full instance lifetime (virtual list reuse can make references stale).
7) Regression tests for transitions: Add tests for the exact transition that previously failed (e.g., storage/category change, plugin removed from report, metered→unmetered, ignoreCase cache warm then parse differently).

Example pattern for superseding async cache updates:
```ts
private _tokenSource?: CancellationTokenSource;
private beginGeneration(): CancellationToken {
  this._tokenSource?.cancel();
  const src = new CancellationTokenSource();
  this._tokenSource = src;
  return src.token;
}

private async refreshForContext(): Promise<void> {
  const token = this.beginGeneration();
  const cachedOrComputed = await this.computeAsync(token);
  if (token.isCancellationRequested) {
    return;
  }
  this.cache = cachedOrComputed;
}
```

Applying these rules prevents stale cache leakage, cache poisoning from incomplete keys, and async late-results overwriting correct state.