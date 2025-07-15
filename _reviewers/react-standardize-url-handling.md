---
title: "Standardize URL handling"
description: "When working with URLs in networking code, always use the standard `URL` constructor to properly resolve relative URLs against a base URL instead of manual string concatenation or ad-hoc replacements."
repository: "facebook/react"
label: "Networking"
language: "JavaScript"
comments_count: 2
repository_stars: 237000
---

When working with URLs in networking code, always use the standard `URL` constructor to properly resolve relative URLs against a base URL instead of manual string concatenation or ad-hoc replacements. This ensures proper path resolution according to the URL specification and handles edge cases correctly.

For example, instead of:
```js
// Problematic: Doesn't properly resolve relative paths
const sourceMap = await fetchFileWithCaching(sourceMapURL).catch(() => null);

// Or hacky string replacements
const normalizedURL = url.replace('/./', '/');
```

Use the URL constructor:
```js
// Properly resolves relative URLs against the base URL
const sourceMap = await fetchFileWithCaching(
  new URL(sourceMapURL, sourceURL).toString()
).catch(() => null);
```

For complex URL normalization needs, consider extracting the logic to a dedicated function that can be maintained centrally and handle different URL formats, including those with custom protocols used by bundlers. This approach prevents networking errors caused by malformed URLs and improves code maintainability.