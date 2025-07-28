---
title: Validate sensitive operations
description: Always implement safety checks before performing operations that could
  expose sensitive data or cause destructive changes. This includes validating targets
  before file deletion and sanitizing credentials in error messages.
repository: prisma/prisma
label: Security
language: TypeScript
comments_count: 2
repository_stars: 42967
---

Always implement safety checks before performing operations that could expose sensitive data or cause destructive changes. This includes validating targets before file deletion and sanitizing credentials in error messages.

For destructive file operations, verify the target contains expected artifacts:
```typescript
// Before deleting, ensure directory contains expected generated files
if (!files.includes('client.d.ts')) {
  throw new Error(
    `${outputDir} exists and is not empty but doesn't look like a generated Prisma Client. ` +
    'Please check your output path and remove the existing directory if you indeed want to generate the Prisma Client in that location.',
  )
}
```

For credential handling, redact sensitive information from logs and error messages:
```typescript
function redactFailedCommand(message: string) {
  // remove the connection url that follows '--datasource' from the given `message`.
  // Note: if the command isn't properly formed, i.e., no connection url follows `--datasource`, we risk redacting an irrelevant part of the command
}
```

This prevents accidental data loss and credential exposure, two common security vulnerabilities that can have severe consequences.