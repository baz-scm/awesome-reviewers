---
title: Normalize URL paths
description: When handling URLs in web applications, consistently normalize path formats
  to prevent routing and service communication issues. This is especially important
  when working with services like Istio that expect specific URL formats (e.g., trailing
  slashes).
repository: kubeflow/kubeflow
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 15064
---

When handling URLs in web applications, consistently normalize path formats to prevent routing and service communication issues. This is especially important when working with services like Istio that expect specific URL formats (e.g., trailing slashes).

Key implementation practices:
1. Ensure URLs end with trailing slashes when required by services
2. Create utility functions to normalize URL paths before comparison
3. Document URL format requirements in code comments

Example:
```typescript
// Ensure trailing slash for service URLs that require it (e.g., Istio)
function normalizeServiceUrl(url: string): string {
  return url?.endsWith('/') ? url : url + '/';
}

// When comparing URLs, normalize paths first
function equalUrlPaths(firstUrl: string, secondUrl: string): boolean {
  // Handle sometimes missing '/' from URLs for consistent comparison
  const normalizedFirst = firstUrl?.endsWith('/') ? firstUrl : firstUrl + '/';
  const normalizedSecond = secondUrl?.endsWith('/') ? secondUrl : secondUrl + '/';
  return normalizedFirst === normalizedSecond;
}
```
