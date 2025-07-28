---
title: Vue syntax parsing robustness
description: When processing Vue components, ensure parsing logic handles edge cases
  correctly and selects appropriate parsers safely. This includes proper validation
  of directive syntax and careful parser selection based on explicit language declarations.
repository: prettier/prettier
label: Vue
language: JavaScript
comments_count: 2
repository_stars: 50772
---

When processing Vue components, ensure parsing logic handles edge cases correctly and selects appropriate parsers safely. This includes proper validation of directive syntax and careful parser selection based on explicit language declarations.

Key considerations:
- Avoid unsafe parser assumptions - TypeScript and JavaScript can parse the same code differently (e.g., `doSomething<T1 | T2>(param)` vs `(doSomething < T1) | (T2 > param)`)
- Only use TypeScript parser when `<script lang="ts">` is explicitly specified
- Handle empty or missing values in directive parsing - don't filter out falsy values that may be semantically meaningful
- Validate directive patterns before processing to prevent undefined returns

Example of problematic parsing:
```javascript
// This should not filter out the empty first iterator
const left = `${[res.alias, res.iterator1, res.iterator2]
  .filter(Boolean)  // ❌ Wrong - removes meaningful empty values
  .join(",")}`;

// For v-for="(,a,b) of 'abcd'" this incorrectly becomes "a,b" instead of ",a,b"
```

Proper validation should check for required components while preserving intentionally empty values in the syntax structure.