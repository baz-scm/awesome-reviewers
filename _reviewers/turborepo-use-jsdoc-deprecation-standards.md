---
title: Use JSDoc deprecation standards
description: When marking code as deprecated, use JSDoc standards to provide clear
  guidance for developers. Always use the `@deprecated` tag followed by when it was
  deprecated and what should be used instead. Additionally, use the `{@link}` tag
  to create clickable references to replacement functionality.
repository: vercel/turborepo
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 28115
---

When marking code as deprecated, use JSDoc standards to provide clear guidance for developers. Always use the `@deprecated` tag followed by when it was deprecated and what should be used instead. Additionally, use the `{@link}` tag to create clickable references to replacement functionality.

Example:
```typescript
/**
 * @deprecated as of Turborepo 2.0.0. Consider using {@link RootSchema.globalDependencies} instead.
 */
export interface SomeDeprecatedInterface {
  // ...
}
```

This approach creates clickable references in many IDEs and documentation tools, allowing developers to quickly navigate to the recommended alternatives. Proper deprecation documentation helps with code maintenance and reduces confusion during migration to newer APIs.