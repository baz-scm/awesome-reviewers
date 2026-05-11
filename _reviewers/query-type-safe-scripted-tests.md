---
title: Type-Safe, Scripted Tests
description: Ensure your testing approach covers both runtime behavior and public
  API types, and that the test scripts you expose are correct, documented, and preserve
  any packaging-specific smoke checks.
repository: tanstack/query
label: Testing
language: Json
comments_count: 3
repository_stars: 49380
---

Ensure your testing approach covers both runtime behavior and public API types, and that the test scripts you expose are correct, documented, and preserve any packaging-specific smoke checks.

Apply this by:
1) Use the right Vitest commands for dev vs CI
- For watch mode, prefer the dedicated watch command.

```json
{
  "scripts": {
    "test:lib": "vitest run",
    "test:lib:dev": "vitest watch"
  }
}
```

2) Make package verification steps explicit (and don’t remove needed checks)
- If a package publishes custom outputs/types (e.g., CJS with custom type shapes), keep a CJS/type smoke check and document what it protects.

3) Add compile-time assertions to type tests
- For hook/type APIs, use `expect-type` (commonly used by Vitest) or equivalent type-testing utilities to assert expected types in type-test files.

```ts
// example pattern for type tests
import { expectTypeOf } from 'expect-type'

expectTypeOf(useSuspenseQuery(/* ... */)).toMatchTypeOf<ExpectedReturnType>()
```

Result: consistent local/dev commands, reliable CI checks, and stronger guarantees that exported APIs behave correctly at both runtime and compile time.