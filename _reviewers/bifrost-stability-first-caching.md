---
title: Stability-First Caching
description: When caching affects externally visible payloads (prompts, auth/JWT inputs,
  token summaries), ensure the *serialized representation used for cache identity
  is deterministic* and the cache has an *explicit validity boundary*.
repository: maximhq/bifrost
label: Caching
language: Go
comments_count: 7
repository_stars: 6862
---

When caching affects externally visible payloads (prompts, auth/JWT inputs, token summaries), ensure the *serialized representation used for cache identity is deterministic* and the cache has an *explicit validity boundary*.

Practical rules:
- **Never rely on Go map iteration order** for data that participates in caching (e.g., JSON used as cache key/prompt identity). Use a deterministic approach:
  - either **preserve ordered structures** end-to-end (e.g., OrderedMap),
  - or **deterministically merge** by inserting keys in sorted order.
- **Keep cache ownership and invalidation triggers consistent** with existing conventions:
  - cache-first only when the in-memory/cache store is the intended hot-path source;
  - evict only when the *downstream system* signals invalid state (e.g., 401/403), not on local token-acquisition errors.
- **Cache hot-path derivatives as immutable snapshots** where possible (e.g., fingerprint provider config paths to avoid per-request file reads) and document that changes at the same path require the designed reload/invalidation mechanism.
- **When reconstructing fields from cached/denormalized data, scope to what your query actually selected**—don’t “fill in” details that weren’t loaded.

Example: deterministic merge without map-key-order instability
```go
func mergeDeterministic(base map[string]any, fallback map[string]any) map[string]any {
	if len(base) == 0 && len(fallback) == 0 {
		return nil
	}
	merged := make(map[string]any, len(base)+len(fallback))

	keys := make([]string, 0, len(base)+len(fallback))
	seen := make(map[string]struct{}, len(base)+len(fallback))
	for k := range base {
		if _, ok := seen[k]; !ok {
			seen[k] = struct{}{}
			keys = append(keys, k)
		}
	}
	for k := range fallback {
		if _, ok := seen[k]; !ok {
			seen[k] = struct{}{}
			keys = append(keys, k)
		}
	}
	sort.Strings(keys)
	for _, k := range keys {
		if v, ok := fallback[k]; ok {
			merged[k] = v
		} else {
			merged[k] = base[k]
		}
	}
	return merged
}
```
If the cached payload must preserve ordering semantics (e.g., `output_config`), prefer an ordered representation (OrderedMap) instead of converting to `map[string]any` during merges.