---
title: Self-referential worker URLs
description: When creating Web Workers for network communication, use self-referential
  URL patterns that are resilient to file renaming. This improves portability and
  reliability of your networking code.
repository: vitejs/vite
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 74031
---

When creating Web Workers for network communication, use self-referential URL patterns that are resilient to file renaming. This improves portability and reliability of your networking code.

For optimal worker initialization, consider these approaches:
- Use the direct self-reference: `new Worker(import.meta.url)`
- Or with explicit URL construction: `new Worker(new URL(import.meta.url))`
- Or using location: `new Worker(self.location.href)`

```javascript
// Recommended approach - resilient to file renaming
const worker = new Worker(new URL(import.meta.url));

// Alternative when referencing other worker files
const worker = new Worker(new URL('./worker.js', import.meta.url));
```

Be aware that when using the same script for both main thread and worker (self-referential pattern), bundlers like Vite will need to bundle the script twice, potentially increasing bundle size but allowing for shared code between contexts.