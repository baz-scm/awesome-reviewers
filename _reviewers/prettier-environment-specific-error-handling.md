---
title: Environment-specific error handling
description: Separate development-time assertions from production error handling based
  on the runtime environment. Development assertions should be used to catch programming
  errors and validate internal assumptions during development, while production code
  should focus on graceful error handling with meaningful user-facing messages.
repository: prettier/prettier
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 50772
---

Separate development-time assertions from production error handling based on the runtime environment. Development assertions should be used to catch programming errors and validate internal assumptions during development, while production code should focus on graceful error handling with meaningful user-facing messages.

Use environment checks to conditionally enable development assertions:

```js
const assertComment = process.env.NODE_ENV === "production" 
  ? noop 
  : function(comment, text) {
      if (!isLineComment(comment) && !isBlockComment(comment)) {
        throw new TypeError(`Unknown comment type: "${comment.type}".`);
      }
    };

// In production, provide simple validation with clear messages
if (!isLineComment(comment) && !isBlockComment(comment)) {
  throw new TypeError(`Unknown comment type: "${comment.type}".`);
}
```

This approach allows comprehensive debugging during development while maintaining clean, user-friendly error handling in production. Configure your build system to remove development-only assertions rather than replacing them with verbose conditional checks that add unnecessary complexity to the codebase.