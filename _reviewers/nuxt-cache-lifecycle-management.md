---
title: Cache lifecycle management
description: Implement comprehensive cache lifecycle management that includes proper
  key management, invalidation strategies, and cleanup mechanisms. Cache implementations
  should handle the full lifecycle from creation to cleanup to prevent memory leaks,
  stale data, and unbounded growth.
repository: nuxt/nuxt
label: Caching
language: TypeScript
comments_count: 4
repository_stars: 57769
---

Implement comprehensive cache lifecycle management that includes proper key management, invalidation strategies, and cleanup mechanisms. Cache implementations should handle the full lifecycle from creation to cleanup to prevent memory leaks, stale data, and unbounded growth.

Key practices:
1. **Proper cache keys**: Use unique, collision-free cache keys and avoid object mutation issues
2. **Invalidation strategies**: Implement TTL mechanisms and handle cache invalidation on updates
3. **Error handling**: Preserve cache-control headers and clear cache on promise rejections
4. **Cleanup mechanisms**: Implement garbage collection for long-lived caches

Example implementation:
```typescript
// Proper cache key management with cleanup
const metaCache = new Map()
const cacheKey = `${absolutePath}:${hash}`

// Handle cache with TTL and error recovery
let manifest: Promise<NuxtAppManifest> | null = null
export function getAppManifest(): Promise<NuxtAppManifest> {
  if (!manifest) {
    manifest = $fetch(manifestUrl).catch(error => {
      manifest = null // Clear on error for retry
      throw error
    })
  }
  return manifest
}

// Preserve cache headers for proper browser caching
setResponseHeaders(event, {
  'Cache-Control': defaultError.headers['cache-control'],
  ...defaultError.headers
})

// Implement GC for build caches
// Keep `.cache/nuxt/builds.json` with id + date for cleanup
```

This approach prevents common caching pitfalls like stale data, memory leaks, and cache corruption while ensuring proper browser caching behavior.