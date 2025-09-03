---
title: Informative error messages
description: Error messages should be informative and include the actual values that
  caused the problem, not just generic descriptions. Use centralized error message
  utilities and ensure both the message and stack trace are properly updated.
repository: cypress-io/cypress
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 48850
---

Error messages should be informative and include the actual values that caused the problem, not just generic descriptions. Use centralized error message utilities and ensure both the message and stack trace are properly updated.

Key practices:
- Include the actual problematic value in error messages (e.g., "expected function, got string" instead of just "expected function")
- Use accurate language that reflects the user's action (e.g., "tried to assign" vs "passed")
- Leverage error utilities like `$errUtils.modifyErrMsg` to ensure consistency between message and stack trace
- Centralize error messages in dedicated files (like error_messages.js) for consistent formatting

Example from the discussions:
```javascript
// Bad - vague and unhelpful
throw new Error('cy.session optional third argument must be an object')

// Good - includes actual problematic value
throw new Error(`cy.session optional third argument must be an object, you passed: ${typeof options}`)

// Better - uses proper error utilities and centralized messages
$errUtils.throwErrByPath('sessions.invalid_options', { 
  args: { expectedType: 'object', actualType: typeof options, actualValue: options } 
})
```

This approach helps developers quickly understand what went wrong and how to fix it, reducing debugging time and improving the development experience.