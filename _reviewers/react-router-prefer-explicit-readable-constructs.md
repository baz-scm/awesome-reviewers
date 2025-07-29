---
title: prefer explicit readable constructs
description: Choose explicit and semantic code constructs that enhance readability
  over more concise but less clear alternatives. This improves code maintainability
  and reduces cognitive load for developers.
repository: remix-run/react-router
label: Code Style
language: TSX
comments_count: 3
repository_stars: 55270
---

Choose explicit and semantic code constructs that enhance readability over more concise but less clear alternatives. This improves code maintainability and reduces cognitive load for developers.

Key practices:
- Use ternary operators instead of `&&` in JSX to make the conditional logic explicit and avoid potential rendering issues
- Use semantic methods like `endsWith()` instead of manual string indexing operations
- Structure complex conditionals with clear if/else branches rather than nested ternaries when there are multiple conditions

Example transformations:
```jsx
// Avoid: && operator in JSX (can cause rendering issues)
{ENABLE_DEV_WARNINGS && heyDeveloper}

// Prefer: explicit ternary
{ENABLE_DEV_WARNINGS ? heyDeveloper : null}

// Avoid: manual string operations
toPathname[toPathname.length - 1] === "/"

// Prefer: semantic methods
toPathname.endsWith("/")
```

This approach makes code intentions clearer, reduces the chance of subtle bugs, and makes the codebase more accessible to developers of varying experience levels.