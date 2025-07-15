---
title: Safe URL operations
description: 'When handling URLs for API interactions and navigation, use precise
  methods for both comparison and construction to avoid subtle bugs:


  1. For URL path comparison, use `startsWith()` instead of `includes()` to prevent
  false positives from substring matches:'
repository: kubeflow/kubeflow
label: API
language: TypeScript
comments_count: 2
repository_stars: 15064
---

When handling URLs for API interactions and navigation, use precise methods for both comparison and construction to avoid subtle bugs:

1. For URL path comparison, use `startsWith()` instead of `includes()` to prevent false positives from substring matches:

```typescript
// AVOID: May lead to incorrect matches
return browserUrl.includes(url);

// BETTER: More precise path matching
return browserUrl.startsWith(url);
```

2. When constructing URLs, use the URL constructor with proper base parameter rather than manual string concatenation:

```typescript
// AVOID: Potential issues with relative paths
const href = window.location.origin + url;
const urlObject = new URL(href);

// BETTER: Robust URL construction
const urlObject = new URL(url, window.location.origin);
```

These practices ensure reliable API interactions and prevent navigation edge cases when handling routes and endpoints.
