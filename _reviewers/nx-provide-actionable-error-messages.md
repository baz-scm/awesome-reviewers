---
title: Provide actionable error messages
description: When handling errors, transform technical exceptions into user-friendly
  messages that include clear remediation steps and actionable guidance. Avoid exposing
  raw technical errors to users, and instead provide context about what went wrong
  and how to resolve the issue.
repository: nrwl/nx
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 27518
---

When handling errors, transform technical exceptions into user-friendly messages that include clear remediation steps and actionable guidance. Avoid exposing raw technical errors to users, and instead provide context about what went wrong and how to resolve the issue.

Rather than letting technical errors bubble up:
```ts
try {
  isNpmInstalled = getPackageManagerVersion('npm', process.cwd(), true) !== '';
} catch (e) {
  throw e; // Raw technical error
}
```

Provide controlled, user-facing error messages:
```ts
try {
  isNpmInstalled = getPackageManagerVersion('npm', process.cwd(), true) !== '';
} catch (e) {
  console.error(`npm was not found in the current environment. This is only supported when using \`bun\` as a package manager, but your detected package manager is "${pm}"`);
  return { success: false };
}
```

Error messages should:
- Explain what went wrong in user terms
- Provide specific remediation steps when possible
- Include relevant context (like detected package manager)
- Mention alternative solutions or workarounds when appropriate
- Guide users to additional resources for verification (e.g., "check the package at npmjs.org")