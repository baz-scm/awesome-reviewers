---
title: Log errors for debugging
description: Always log errors in catch blocks and use named functions to improve
  debugging and error traceability. Empty catch blocks make it impossible to diagnose
  issues, while anonymous functions provide poor stack traces.
repository: discourse/discourse
label: Error Handling
language: Other
comments_count: 2
repository_stars: 44898
---

Always log errors in catch blocks and use named functions to improve debugging and error traceability. Empty catch blocks make it impossible to diagnose issues, while anonymous functions provide poor stack traces.

When handling exceptions, capture and log the error details to the console so developers have actionable information when things go wrong. Additionally, name your functions instead of using anonymous exports to improve backtraces and error messages.

Example of proper error logging:
```javascript
// Bad - silent failure
try {
  await clipboardCopy(this.args.colorPalette.dump());
} catch {
  this.toasts.error({ data: { message: "Copy failed" } });
}

// Good - log error details
try {
  await clipboardCopy(this.args.colorPalette.dump());
} catch (error) {
  // eslint-disable-next-line no-console
  console.error(error);
  this.toasts.error({ data: { message: "Copy failed" } });
}
```

Example of named functions for better debugging:
```javascript
// Bad - anonymous function
export default function (element, context) {
  // ...
}

// Good - named function improves backtraces
export default function quoteControls(element, context) {
  // ...
}
```

This practice ensures that when errors occur, developers have the necessary context and information to diagnose and fix issues quickly.