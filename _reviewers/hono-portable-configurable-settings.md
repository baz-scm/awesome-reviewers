---
title: Portable, configurable settings
description: When reading environment variables or runtime-specific context, avoid
  relying on globals or platform-specific APIs that only work on one runtime (e.g.,
  `globalThis.process`, `c.env` on Cloudflare Workers). Instead, use the shared, runtime-agnostic
  abstraction provided by the framework (e.g., `env()` from `hono/adapter`) so the
  same code works consistently...
repository: honojs/hono
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 32741
---

When reading environment variables or runtime-specific context, avoid relying on globals or platform-specific APIs that only work on one runtime (e.g., `globalThis.process`, `c.env` on Cloudflare Workers). Instead, use the shared, runtime-agnostic abstraction provided by the framework (e.g., `env()` from `hono/adapter`) so the same code works consistently across Node, Deno, Cloudflare Workers, and other targets. If a runtime-specific check is truly unavoidable (e.g., due to a temporary platform limitation), document the reason clearly and revisit it once the limitation is resolved.

Additionally, avoid hardcoding values that represent configurable behavior (such as fixed lists of headers, flags, or thresholds) directly in the implementation. Expose them as options with sensible defaults so consumers can override or extend them without modifying the library code.

Example:
```ts
// Avoid: hardcoded, non-overridable list
const RETAINED_304_HEADERS = ['cache-control', 'content-location', 'date', 'etag', 'expires', 'vary']

// Prefer: configurable via options
type ETagOptions = {
  weak: boolean
  retainedHeaders?: string[]
}
const DEFAULT_RETAINED_304_HEADERS = ['cache-control', 'content-location', 'date', 'etag', 'expires', 'vary']

function etag(options: ETagOptions) {
  const retainedHeaders = options.retainedHeaders ?? DEFAULT_RETAINED_304_HEADERS
  // ...
}
```

Applying this standard keeps configuration logic portable across environments and flexible for consumers, reducing the need for future breaking changes or runtime-specific workarounds.