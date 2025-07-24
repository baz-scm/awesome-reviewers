---
title: Use TypeScript-specific tests
description: 'Always use fourslash tests (for IDE/language service features) or compiler
  tests (for TypeScript compilation behavior) instead of direct unit tests. Place
  tests in the correct directories: `tests/cases/compiler` or `tests/cases/fourslash`.'
repository: microsoft/typescript
label: Testing
language: Markdown
comments_count: 2
repository_stars: 105378
---

Always use fourslash tests (for IDE/language service features) or compiler tests (for TypeScript compilation behavior) instead of direct unit tests. Place tests in the correct directories: `tests/cases/compiler` or `tests/cases/fourslash`.

Fourslash tests validate IDE features like completions and refactoring:

```typescript
/// <reference path='fourslash.ts'/>

//// interface User {
////     name: string;
//// }
//// 
//// const user: User = {
////     /*completion*/
//// };

verify.completions({
    marker: "completion",
    includes: { name: "name" }
});
```

Compiler tests validate TypeScript type checking:

```typescript
// @Filename: test.ts
// @strict: true

interface Config {
    required: string;
    optional?: number;
}

const config1: Config = { required: "test" }; // Should work
const config2: Config = { optional: 42 }; // Should error - missing required
```

When adding tests, ensure you run them individually first with `hereby runtests --tests=path/to/test.ts` to verify they demonstrate the expected behavior correctly before committing.