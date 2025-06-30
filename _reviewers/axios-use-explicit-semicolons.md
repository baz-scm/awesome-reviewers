---
title: Use explicit semicolons
description: Always terminate statements with explicit semicolons rather than relying
  on JavaScript's automatic semicolon insertion (ASI). This ensures consistency with
  the existing codebase where 93-97% of statements already use explicit semicolons.
repository: axios/axios
label: Code Style
language: Javascript
comments_count: 4
repository_stars: 107146
---

Always terminate statements with explicit semicolons rather than relying on JavaScript's automatic semicolon insertion (ASI). This ensures consistency with the existing codebase where 93-97% of statements already use explicit semicolons.

Relying on ASI can lead to unexpected behavior and makes the code harder to maintain, especially for developers who are unfamiliar with all ASI rules. It also helps prevent potential bugs that could occur when code is minified or combined with other scripts.

Example of incorrect code:
```javascript
const brotliOptions = {
  flush: zlib.constants.BROTLI_OPERATION_FLUSH,
  finishFlush: zlib.constants.BROTLI_OPERATION_FLUSH
} // Missing semicolon

if (proxy.servername) {
  options.servername = proxy.servername // Missing semicolon
}
```

Example of correct code:
```javascript
const brotliOptions = {
  flush: zlib.constants.BROTLI_OPERATION_FLUSH,
  finishFlush: zlib.constants.BROTLI_OPERATION_FLUSH
}; // Added explicit semicolon

if (proxy.servername) {
  options.servername = proxy.servername; // Added explicit semicolon
}
```

## Discussions

