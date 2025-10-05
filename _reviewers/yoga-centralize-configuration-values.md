---
title: Centralize configuration values
description: Consolidate all configuration variables, constants, and settings into
  a centralized configuration object rather than declaring them as scattered variables
  throughout the codebase. This improves maintainability, reduces duplication, and
  enables consistent templating patterns.
repository: facebook/yoga
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 18255
---

Consolidate all configuration variables, constants, and settings into a centralized configuration object rather than declaring them as scattered variables throughout the codebase. This improves maintainability, reduces duplication, and enables consistent templating patterns.

Instead of defining variables separately:
```javascript
var cTestClean, cTestCompile, cTestExecute;
var pathDelimiter = path.delimiter;
```

Add them to your config object:
```javascript
var config = {
  libName: 'css-layout',
  distFolder: 'dist',
  srcFolder: 'src',
  cTestClean: '...',
  cTestCompile: '...',
  cTestExecute: '...',
  pathDelimiter: path.delimiter
};
```

This allows for consistent templating usage like `<%= config.pathDelimiter %>` instead of mixing template strings with concatenation, and keeps all configuration in one discoverable location.