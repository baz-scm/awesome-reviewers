---
title: Semantic naming conventions
description: Use names that clearly convey the purpose and content of variables, parameters,
  and properties. When working with objects, always access specific properties rather
  than using the object directly in string operations to prevent "[object Object]"
  outputs. Include proper type declarations for parameters that describe their structure.
repository: vercel/turborepo
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 28115
---

Use names that clearly convey the purpose and content of variables, parameters, and properties. When working with objects, always access specific properties rather than using the object directly in string operations to prevent "[object Object]" outputs. Include proper type declarations for parameters that describe their structure.

Example:
```typescript
// Incorrect
function replacePackageManager(packageManager, text) {
  const updatedText = match.replace(replacementRegex, `${packageManager} run`);
  // Results in "[object Object] run"
}

// Correct
function replacePackageManager(packageManager: { name: string }, text: string): string {
  const updatedText = match.replace(replacementRegex, `${packageManager.name} run`);
  // Results in "npm run" or similar
}

// Improved parameter naming
affectedPackages(
  files: Array<string>,
  base?: string | undefined | null, // "base" clearly indicates this is the base commit for comparison
)
```

Choose parameter names that use domain-specific terminology where appropriate to make code more self-documenting and easier to understand.