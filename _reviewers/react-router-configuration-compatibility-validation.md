---
title: configuration compatibility validation
description: Ensure that code examples and documentation accurately reflect the constraints
  and requirements of different rendering modes and configurations. When documenting
  APIs or providing examples, verify that the suggested approach is compatible with
  the specific rendering context (SSR, SSG, client-side) and configuration options
  being used.
repository: remix-run/react-router
label: Next
language: Markdown
comments_count: 6
repository_stars: 55270
---

Ensure that code examples and documentation accurately reflect the constraints and requirements of different rendering modes and configurations. When documenting APIs or providing examples, verify that the suggested approach is compatible with the specific rendering context (SSR, SSG, client-side) and configuration options being used.

Key areas to validate:
- API compatibility with rendering modes (e.g., certain rendering methods may not work with specific fetch strategies)
- Accurate terminology that doesn't make assumptions about HTTP status codes or behavior
- Clear distinction between different configuration options and their use cases
- Proper explanation of when certain features or patterns should be used

Example of problematic documentation:
```tsx
// Incorrect - renderToString may not work with single fetch
export default function handleRequest(request, responseStatusCode, responseHeaders, routerContext) {
  const markup = renderToString(/* ... */);
}
```

Example of improved documentation:
```tsx
// Correct - acknowledges configuration constraints
export default function handleRequest(request, responseStatusCode, responseHeaders, routerContext) {
  // Note: When using single fetch, use appropriate rendering method
  // for your configuration. See [link] for compatible options.
  const markup = renderToReadableStream(/* ... */);
}
```

This validation helps prevent runtime errors and ensures developers can successfully implement the documented patterns in their specific environment.