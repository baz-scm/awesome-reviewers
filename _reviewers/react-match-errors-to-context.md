---
title: "Match errors to context"
description: "Choose error handling mechanisms based on the error's severity and context. For critical issues that should prevent further execution, throw explicit exceptions. For non-critical issues, use logging with sufficient detail to aid debugging without interrupting execution."
repository: "facebook/react"
label: "Error Handling"
language: "TypeScript"
comments_count: 3
repository_stars: 237000
---

Choose error handling mechanisms based on the error's severity and context. For critical issues that should prevent further execution, throw explicit exceptions. For non-critical issues, use logging with sufficient detail to aid debugging without interrupting execution.

When throwing exceptions for critical validation errors:
```ts
if (reference.resolved === null) {
  throw new Error('Unexpected undefined reference.resolved');
}
```

When logging non-critical issues, include precise location information and use visual indicators to distinguish error types:
```ts
const { reason, severity, loc } = compilation.detail;
const lnNo = loc.start?.line;
const colNo = loc.start?.column;
const isTodo = severity === ErrorSeverity.Todo;

console.log(
  chalk[isTodo ? 'yellow' : 'red'](
    `Failed to compile ${filename}${lnNo !== undefined ? `:${lnNo}${colNo !== undefined ? `:${colNo}` : ""}` : ""}`
  ),
  reason ? `\n  Reason: ${isTodo ? 'Unimplemented' : reason}` : ""
);
```

This approach helps identify bugs early in the development process for critical issues while providing informative, actionable feedback for less severe problems without unnecessarily halting execution.