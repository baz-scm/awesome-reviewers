---
title: Handle SSR hydration mismatches
description: When implementing server-side rendering, proactively handle scenarios
  where server and client rendering may produce different outputs to prevent hydration
  errors. This commonly occurs with dynamic URLs, route matching, and encoded characters.
repository: remix-run/react-router
label: Next
language: TSX
comments_count: 2
repository_stars: 55270
---

When implementing server-side rendering, proactively handle scenarios where server and client rendering may produce different outputs to prevent hydration errors. This commonly occurs with dynamic URLs, route matching, and encoded characters.

Implement defensive coding practices that gracefully handle these mismatches:

1. **Clear conflicting server state** when client routing takes precedence:
```javascript
// Clear SSR 404s when client routes match
if (matchedPropRoute) {
  for (let [routeId, error] of Object.entries(hydrationData.errors)) {
    if (isRouteErrorResponse(error) && error.status === 404) {
      delete hydrationData.errors[routeId];
    }
  }
}
```

2. **Normalize URLs** to match client-side encoding:
```javascript
function safelyEncodeSsrHref(to: To, href: string): string {
  let path = typeof to === "string" ? parsePath(to).pathname : to.pathname;
  if (!path || path === ".") {
    try {
      let encoded = new URL(href, "http://localhost");
      return encoded.pathname + encoded.search;
    } catch (e) {
      // no-op - no changes if we can't construct a valid URL
    }
  }
  return href;
}
```

While some hydration flickering may be unavoidable in edge cases, proper error handling ensures the application recovers gracefully and maintains functionality.