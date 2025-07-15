---
title: Document with precise accuracy
description: Maintain precise and accurate documentation through both JSDoc annotations
  and explanatory comments. Ensure all technical documentation matches the actual
  implementation, avoiding inconsistencies between code and documentation.
repository: nodejs/node
label: Documentation
language: JavaScript
comments_count: 5
repository_stars: 112178
---

Maintain precise and accurate documentation through both JSDoc annotations and explanatory comments. Ensure all technical documentation matches the actual implementation, avoiding inconsistencies between code and documentation.

Key practices:
1. Keep JSDoc parameter and return types strictly accurate
2. Avoid default values in JSDoc to prevent inconsistencies
3. Document unusual patterns or complex implementations
4. Include clear examples for non-obvious functionality

Example:
```javascript
/**
 * Format help text for printing.
 * @param {string} longOption - long option name e.g. 'foo'
 * @param {object} optionConfig - option config from parseArgs({ options })
 * @returns {string} formatted help text for printing
 * @example
 * formatHelpTextForPrint('foo', { type: 'string', help: 'help text' })
 * // returns '--foo <arg>                   help text'
 */
function formatHelpTextForPrint(longOption, optionConfig) {
  // Implementation using unusual pattern - explain why
  if (isSpecialCase(optionConfig)) {
    // Document why this special case exists
    // and how it affects the output
  }
  // ... rest of implementation
}