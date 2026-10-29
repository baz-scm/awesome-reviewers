---
title: Consistent lint-compliant style
description: 'Follow the project''s established linting and formatting conventions
  consistently rather than introducing one-off styles:


  1. Always use curly braces for conditionals, even single-line ones, to match the
  project''s `curly: all` rule:'
repository: honojs/Hono
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 32741
---

Follow the project's established linting and formatting conventions consistently rather than introducing one-off styles:

1. Always use curly braces for conditionals, even single-line ones, to match the project's `curly: all` rule:
```ts
// Good
if (!location) {
  return false
}

// Avoid
if (!location) return false
```

2. Combine multiple imports from the same module into a single statement instead of separate import lines:
```ts
// Good
import { parseBody, type BodyData } from './body'

// Avoid
import { parseBody } from './body'
import type { BodyData } from './body'
```

3. Use dedicated type-only import/export syntax rather than inline `type` keyword inside braces, for clarity and consistency:
```ts
// Good
export { handle, streamHandle } from './handler'
export type { APIGatewayProxyResult } from './handler'

// Avoid
export { handle, streamHandle, type APIGatewayProxyResult } from './handler'
```

4. Remove unused parameters/variables entirely instead of keeping them with `eslint-disable` comments, unless they are required to satisfy an interface signature:
```ts
// Good
protected getQueryString(): string {
  return ''
}

// Avoid
// eslint-disable-next-line @typescript-eslint/no-unused-vars
protected getQueryString(event: LatticeProxyEventV2): string {
  return ''
}
```

5. Keep casing of well-known terms (e.g., `ETag`, `JWK`) consistent throughout code and tests, even though some identifiers like HTTP headers are case-insensitive at runtime.

When Prettier and ESLint rules conflict (e.g., quote styles), resolve the conflict explicitly with a scoped `// eslint-disable-next-line <rule>` comment rather than letting CI fail, and consider fixing the underlying ESLint config if the conflict is systemic. Applying these conventions uniformly keeps the codebase readable, avoids noisy diffs, and prevents lint/CI friction during review.