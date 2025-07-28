---
title: defensive null checking
description: Implement robust null and undefined handling patterns to prevent runtime
  errors and maintain code reliability. Use optional chaining for safe property access,
  explicit null checks with early returns, and conditional property assignment to
  avoid unintended undefined values.
repository: electron/electron
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 117644
---

Implement robust null and undefined handling patterns to prevent runtime errors and maintain code reliability. Use optional chaining for safe property access, explicit null checks with early returns, and conditional property assignment to avoid unintended undefined values.

Key patterns to follow:
- Use optional chaining (`?.`) when accessing properties that might be undefined: `if (options?.throwIfNoEntry === true)`
- Add explicit null checks with early returns to fail fast: `if (!webContents) return null;`
- Use conditional assignment or property existence checks to preserve intended default values instead of unconditionally assigning potentially undefined values

Example implementation:
```ts
// Good: Optional chaining and explicit null check
const archive = getOrCreateArchive(asarPath);
if (!archive) {
  if (options?.throwIfNoEntry === true) {
    throw createError(AsarError.INVALID_ARCHIVE, { asarPath });
  }
  return null;
}

// Good: Conditional property assignment to preserve defaults
const urlLoaderOptions = {
  priority: options.priority
};
if ('priorityIncremental' in options) {
  urlLoaderOptions.priorityIncremental = options.priorityIncremental;
}
```

This approach prevents silent failures, maintains type safety, and ensures predictable behavior when dealing with nullable values.