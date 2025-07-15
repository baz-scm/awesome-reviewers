---
title: "Proper Usage of React Hooks"
description: "When using the React library in TypeScript, ensure that you are correctly implementing the recommended React hooks based on the version of ESLint being used in your project."
repository: "facebook/react"
label: "React"
language: "TypeScript"
comments_count: 2
repository_stars: 237000
---

When using the React library in TypeScript, ensure that you are correctly implementing the recommended React hooks based on the version of ESLint being used in your project.

For projects using ESLint 9.0.0 and above, use the `recommended-latest` configuration for the `react-hooks` plugin. This will enforce the latest best practices for React hook usage.

For projects using ESLint versions below 9.0.0, use the `recommended-legacy` configuration for the `react-hooks` plugin. This will ensure compatibility with older versions of React and ESLint.

Example of correct usage:

```typescript
// For ESLint 9.0.0+
{
  "extends": [
    // ...
    "plugin:react-hooks/recommended-latest"
  ]
}

// For ESLint below 9.0.0 
{
  "extends": [
    // ...
    "plugin:react-hooks/recommended-legacy"
  ]
}
```

Avoid using deprecated configuration names like the plain `recommended`, even if they are still supported for backward compatibility. Always use the version-specific configurations to ensure your React code follows the latest best practices and remains compatible with the ESLint version in use.