---
title: Purposeful style changes
description: Code style modifications should accompany functional improvements rather
  than being submitted as standalone changes. When improving code, prefer modern JavaScript
  syntax like object spread over older patterns or external dependencies.
repository: expressjs/express
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 67300
---

Code style modifications should accompany functional improvements rather than being submitted as standalone changes. When improving code, prefer modern JavaScript syntax like object spread over older patterns or external dependencies.

Example:
```js
// Instead of using external dependencies:
const merged = require('utils-merge')(obj1, obj2);

// Prefer native JavaScript features:
const merged = {...obj1, ...obj2};
```

The project prioritizes meaningful contributions that improve functionality or fix issues over purely cosmetic changes. Pull requests focused solely on code style updates without functional benefits are generally not accepted.