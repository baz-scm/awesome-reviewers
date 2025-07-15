---
title: Opt-in configurable caching
description: Implement caching mechanisms as opt-in features with explicit configuration
  options rather than as defaults. This approach prevents unexpected behavior and
  allows teams to deliberately enable caching where beneficial.
repository: grafana/grafana
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 68825
---

Implement caching mechanisms as opt-in features with explicit configuration options rather than as defaults. This approach prevents unexpected behavior and allows teams to deliberately enable caching where beneficial.

Key implementation guidelines:
- Only cache successful responses, not error states
- Design cache placement to prevent redundant requests
- Consider strategies like debouncing to prevent multiple identical requests
- Provide mechanisms to avoid conflicts with existing caching layers

Example implementation:
```typescript
export function runRequest(
  datasourceRequest: DataQueryRequest,
  options: RunRequestOptions = {}
): Observable<PanelData> {
  // Cache configuration with defaults
  const cacheConfig = {
    enabled: options.enableCache ?? false,
    cacheErrorResponses: false,
    // other cache options
  };

  // Generate cache key only if caching is enabled
  const cacheKey = cacheConfig.enabled ? generateCacheKey(datasourceRequest) : null;
  
  // Check cache first if enabled
  if (cacheConfig.enabled && cacheKey && cache.has(cacheKey)) {
    return of(cache.get(cacheKey));
  }
  
  // Proceed with request
  // ...
  
  // Only cache successful responses
  if (cacheConfig.enabled && cacheKey && !state.panelData.error) {
    cache.set(cacheKey, state.panelData);
  }
}
```

This approach allows for shared caching across different parts of the application while avoiding the pitfall of multiple layers of cache that could lead to cache invalidation challenges.