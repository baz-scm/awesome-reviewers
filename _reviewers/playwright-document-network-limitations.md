---
title: Document network limitations
description: When documenting network-related features, clearly specify compatibility
  constraints, browser limitations, and potential side effects. This is especially
  critical for experimental features or those with platform-specific restrictions.
repository: microsoft/playwright
label: Networking
language: Markdown
comments_count: 2
repository_stars: 76113
---

When documenting network-related features, clearly specify compatibility constraints, browser limitations, and potential side effects. This is especially critical for experimental features or those with platform-specific restrictions.

Always include:
- Explicit browser/platform compatibility information
- Warnings for experimental features that may change
- Known limitations and their impact on functionality
- Potential side effects (e.g., CORS implications, header modifications)

Example:
```ts
// Good: Clear limitations and warnings
/**
 * Mocking proxy is **experimental** and subject to change.
 * Limitations:
 * - Extra headers will affect CORS preflight requests
 * - Server requests not triggered by browser won't be routed
 * - Only works with persistent browser contexts
 */
export default defineConfig({
  use: { mockingProxy: true }
});
```

This prevents user confusion, reduces support burden, and helps developers make informed decisions about feature adoption.