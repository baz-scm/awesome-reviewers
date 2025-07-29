---
title: use modern JavaScript patterns
description: Adopt modern JavaScript syntax and patterns to improve code quality and
  maintainability. This includes using current language features over deprecated alternatives,
  proper variable declarations, and modern conditional operators.
repository: remix-run/react-router
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 55270
---

Adopt modern JavaScript syntax and patterns to improve code quality and maintainability. This includes using current language features over deprecated alternatives, proper variable declarations, and modern conditional operators.

Key practices to follow:
- Replace deprecated methods like `substr()` with modern equivalents like `substring()`
- Use `const` instead of `let` when variables won't be reassigned
- Prefer optional chaining (`?.`) and ternary operators over logical AND (`&&`) in JSX conditional rendering
- Follow established best practices for conditional rendering patterns

Example of improved JSX conditional rendering:
```tsx
// Instead of:
{actionData && actionData.error && (
  <div>Error occurred</div>
)}

// Use:
{actionData?.error ? (
  <div>Error occurred</div>
) : null}
```

This approach reduces potential runtime errors, improves readability, and follows current JavaScript and React best practices.