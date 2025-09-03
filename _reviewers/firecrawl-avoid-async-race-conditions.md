---
title: Avoid async race conditions
description: Ensure proper async/await handling and consider concurrent execution
  patterns to prevent race conditions and improve performance. When working with asynchronous
  operations, always use await for promises and avoid mixing promise chains with async/await
  syntax. Additionally, identify opportunities to run independent operations concurrently
  rather than...
repository: firecrawl/firecrawl
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Ensure proper async/await handling and consider concurrent execution patterns to prevent race conditions and improve performance. When working with asynchronous operations, always use await for promises and avoid mixing promise chains with async/await syntax. Additionally, identify opportunities to run independent operations concurrently rather than sequentially.

Common issues to watch for:
- Missing await keywords on promise-returning functions
- Dynamic imports without proper await handling
- Sequential execution of independent async operations

Example of problematic code:
```typescript
private static loadWebSocket() {
  try {
    return require('isows').WebSocket;
  } catch {
    try {
      return import('isows').then(m => m.WebSocket); // Missing await, can cause race condition
    } catch {
      // fallback
    }
  }
}
```

Better approach:
```typescript
private static async loadWebSocket() {
  try {
    return require('isows').WebSocket;
  } catch {
    try {
      const module = await import('isows'); // Proper await handling
      return module.WebSocket;
    } catch {
      // fallback
    }
  }
}
```

For independent operations, prefer concurrent execution:
```typescript
// Instead of sequential
const sitemapLinks1 = await this.tryFetchSitemapLinks(url, "/sitemap.xml");
const sitemapLinks2 = await this.tryFetchSitemapLinks(url, "/sitemap_index.xml");

// Use concurrent execution
const [sitemapLinks1, sitemapLinks2] = await Promise.all([
  this.tryFetchSitemapLinks(url, "/sitemap.xml"),
  this.tryFetchSitemapLinks(url, "/sitemap_index.xml")
]);
```