---
title: ESLint configuration alignment
description: Ensure your ESLint configuration matches the JavaScript language features
  used in your codebase to prevent false warnings and maintain consistent code quality
  checks. When using ES6+ features like `let`, `const`, object shorthand notation,
  or other modern JavaScript syntax, update your ESLint configuration to recognize
  these features.
repository: adonisjs/core
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 18071
---

Ensure your ESLint configuration matches the JavaScript language features used in your codebase to prevent false warnings and maintain consistent code quality checks. When using ES6+ features like `let`, `const`, object shorthand notation, or other modern JavaScript syntax, update your ESLint configuration to recognize these features.

Common symptoms of misaligned configuration include warnings like "'let' is available in ES6 (use esnext option)" or "'const' is available in ES6" when these features are intentionally used in the code.

Example configuration fix:
```javascript
// .eslintrc.js
module.exports = {
  "parserOptions": {
    "ecmaVersion": 6, // or higher for newer features
    "sourceType": "module"
  },
  "env": {
    "es6": true,
    "node": true
  }
};
```

This prevents the need for eslint-disable comments and ensures your linting rules accurately reflect your coding standards rather than generating noise from outdated configuration settings.