---
title: Respect lint and syntax conventions
description: Before introducing newer JavaScript syntax (ES6 classes, multiple `const`
  declarations, spread operators, template literals, etc.), verify it is actually
  supported by the project's configured linter and target Node/runtime compatibility.
  Several PRs had to be reverted or reworked because `eslint` rejected classes, template
  literals, or spread syntax that...
repository: Expressjs/Express
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 69580
---

Before introducing newer JavaScript syntax (ES6 classes, multiple `const` declarations, spread operators, template literals, etc.), verify it is actually supported by the project's configured linter and target Node/runtime compatibility. Several PRs had to be reverted or reworked because `eslint` rejected classes, template literals, or spread syntax that the `main`/compatibility branch does not yet support (e.g. `const express = require('../..'), bodyParser = require('body-parser')...` had to be split into separate `const` statements per the `standard` style guide; a `const { ...this.locals, ...opts }` spread had to fall back to `Object.assign` until the lint config is upgraded). If a desired modern syntax isn't supported, use the older equivalent (`var`, `Object.assign`, string concatenation) and note the lint/config upgrade as a separate follow-up rather than mixing styles in the same PR.

In addition, keep code idiomatic and non-duplicated:
- Prefer standard idioms already used elsewhere in the codebase (e.g. `Array.isArray(x)` instead of `x instanceof Array`, `typeof fn === 'function'` instead of `Object.prototype.toString.call(fn)`).
- Factor out duplicated expressions or object literals into a shared variable/constant instead of repeating the same check or literal multiple times (e.g. `var isChunkBlob = chunk instanceof Blob` computed once and reused, or reusing one `{ expires: new Date(1), path: '/' }` object instead of maintaining two copies).

Example:
```js
// Bad: duplicated literal/check, and mixed/unsupported syntax
var opts = options
  ? merge({ expires: new Date(1), path: '/' }, options)
  : { expires: new Date(1), path: '/' };

// Good: single source of truth, syntax matching project's supported style
var defaults = { expires: new Date(1), path: '/' };
var opts = options ? merge(defaults, options) : defaults;
```

Applying this consistently keeps the codebase compatible with its target environment, avoids CI/lint failures, and makes code easier to read and maintain.