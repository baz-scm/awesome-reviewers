---
title: Consistent descriptive identifiers
description: Use camelCase for all variables, parameters, methods, and functions in
  JavaScript/TypeScript code to maintain consistency with language conventions. Choose
  names that accurately describe the purpose and behavior of identifiers, and avoid
  naming collisions between different scopes.
repository: oven-sh/bun
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 79093
---

Use camelCase for all variables, parameters, methods, and functions in JavaScript/TypeScript code to maintain consistency with language conventions. Choose names that accurately describe the purpose and behavior of identifiers, and avoid naming collisions between different scopes.

**Do this:**
```typescript
interface CSVParserOptions {
  header?: boolean;
  delimiter?: string;
  trimWhitespace?: boolean; // camelCase instead of snake_case
  dynamicTyping?: boolean;  // camelCase instead of snake_case
}

function diagnose(
  fixtureDir: string,
  config: {
    options?: Partial<ts.CompilerOptions>;
    extraFiles?: Record<string, string>; // Clear, descriptive name that won't conflict
  } = {},
) {
  const tsconfig = config.options ?? {};
  const extraFiles = config.extraFiles;
  // ...
}
```

**Don't do this:**
```typescript
interface CSVParserOptions {
  header?: boolean;
  delimiter?: string;
  trim_whitespace?: boolean; // Inconsistent with JS/TS conventions
  dynamic_typing?: boolean;  // Inconsistent with JS/TS conventions
}

function diagnose(
  fixtureDir: string,
  config: {
    options?: Partial<ts.CompilerOptions>;
    files?: Record<string, string>; // Could conflict with local variables
  } = {},
) {
  const tsconfig = config.options ?? {};
  const files = config.files;
  // Can lead to confusion with other 'files' variables in the function
}
```

Avoid unused identifiers, or clearly document why they're being parsed but not used. Choose names that accurately reflect the behavior of functions rather than their implementation details to improve code readability and maintainability.