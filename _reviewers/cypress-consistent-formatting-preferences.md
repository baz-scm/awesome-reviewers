---
title: Consistent formatting preferences
description: Follow consistent formatting and syntax patterns to improve code readability
  and maintainability. This includes using compact formatting for test blocks, proper
  quote usage, positive-first conditionals, and preferred syntax patterns.
repository: cypress-io/cypress
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 48850
---

Follow consistent formatting and syntax patterns to improve code readability and maintainability. This includes using compact formatting for test blocks, proper quote usage, positive-first conditionals, and preferred syntax patterns.

Key formatting guidelines:
- Use compact formatting for describe/it blocks: `describe('errors', { defaultCommandTimeout: 50 }, () => {`
- Prefer double quotes over escaped single quotes: `"foo"` instead of `'foo\'`  
- Put positive conditions first in if statements: `if (state.initialBuildSucceed) { ... } else { ... }`
- Use direct return expressions: `return (expression)` instead of `if (...) return true`
- Prefer `.catch()` syntax over try/catch blocks for promise handling
- Use proper eslint disable patterns: `/* global jest */` at file top instead of inline `eslint-disable-next-line no-undef`

These patterns make code more readable and follow modern JavaScript conventions while reducing cognitive load for developers.