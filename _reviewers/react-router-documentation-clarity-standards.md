---
title: documentation clarity standards
description: Ensure all React-related documentation, comments, and descriptions maintain
  high standards of clarity, accuracy, and consistency. This includes using proper
  grammar, consistent terminology, complete descriptions, and well-structured explanations.
repository: remix-run/react-router
label: React
language: Markdown
comments_count: 30
repository_stars: 55270
---

Ensure all React-related documentation, comments, and descriptions maintain high standards of clarity, accuracy, and consistency. This includes using proper grammar, consistent terminology, complete descriptions, and well-structured explanations.

Key areas to focus on:

1. **Grammar and Structure**: Use proper grammar, punctuation, and sentence structure. Avoid incomplete sentences or unclear phrasing.

2. **Terminology Consistency**: Use consistent and accurate technical terms throughout. For example, prefer "Route Module API" over "Route Modules" when referring to the specific API, or "RSC-compatible bundlers" instead of "RSC-native bundlers" when the terminology is more accurate.

3. **Complete Descriptions**: Provide thorough explanations rather than abbreviated or incomplete descriptions. Changeset descriptions should clearly explain what changed and why.

4. **Code Example Accuracy**: Ensure code examples are syntactically correct and demonstrate best practices. Use proper destructuring, correct function signatures, and appropriate file extensions.

Example of improved documentation:

```tsx
// Before: Incomplete and unclear
export function routes() {
  // Route Modules have been a Framework Mode only feature
}

// After: Clear and complete  
export function routes() {
  // The Route Module API has been a Framework Mode only feature
  // until now, but the lazy field unifies the APIs
}
```

This standard helps maintain professional documentation quality that makes React applications more maintainable and easier for developers to understand and contribute to.