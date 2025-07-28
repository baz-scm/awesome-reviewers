---
title: Maintain naming consistency
description: Ensure consistent naming patterns and approaches across similar functionality
  in the codebase. This includes using named constants instead of magic strings, aligning
  input handling patterns with existing code, maintaining consistent identifier formats,
  and following established conventions from libraries or existing implementations.
repository: google-gemini/gemini-cli
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 65062
---

Ensure consistent naming patterns and approaches across similar functionality in the codebase. This includes using named constants instead of magic strings, aligning input handling patterns with existing code, maintaining consistent identifier formats, and following established conventions from libraries or existing implementations.

Key practices:
- Replace magic string literals with named constants: `const CLEAR_QUEUE_SIGNAL = '__CLEAR_QUEUE__'` instead of using the raw string
- Align naming patterns with existing code: use consistent approaches for similar functionality like keyboard input handling
- Maintain consistent identifier formats: ensure prompt IDs, session IDs follow the same naming conventions across the codebase
- Follow established library conventions: when adding new functionality, match the patterns already used by existing libraries or components

Example from the discussions:
```typescript
// Before: Magic string
if (trimmedValue === '__CLEAR_QUEUE__') {
  setQueuedInput(null);
  return;
}

// After: Named constant
import { CLEAR_QUEUE_SIGNAL } from './constants.js';
if (trimmedValue === CLEAR_QUEUE_SIGNAL) {
  setQueuedInput(null);
  return;
}
```

This approach improves code maintainability, reduces errors from typos in magic strings, and makes the codebase more predictable for developers working across different modules.