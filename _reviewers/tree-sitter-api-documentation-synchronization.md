---
title: API documentation synchronization
description: Ensure that all API documentation, including code examples and integration
  guides, accurately reflects the current API state. When API changes occur (such
  as import/export modifications, new entry points, or version compatibility updates),
  corresponding documentation must be updated immediately to prevent developer confusion
  and integration errors.
repository: tree-sitter/tree-sitter
label: API
language: Markdown
comments_count: 2
repository_stars: 21799
---

Ensure that all API documentation, including code examples and integration guides, accurately reflects the current API state. When API changes occur (such as import/export modifications, new entry points, or version compatibility updates), corresponding documentation must be updated immediately to prevent developer confusion and integration errors.

Key areas to verify:
- Import/export syntax matches current API structure
- All available API entry points and variants are documented
- Version-specific compatibility information is accurate and up-to-date
- Integration examples work with the documented API version

Example of outdated documentation that needs correction:
```js
// Outdated - no longer works
import Parser from 'web-tree-sitter';

// Current - matches actual API
import { Parser } from 'web-tree-sitter';
// Also document available variants
import { Parser } from 'web-tree-sitter/debug';
```

This practice prevents developers from encountering runtime errors due to mismatched documentation and ensures smooth API adoption.