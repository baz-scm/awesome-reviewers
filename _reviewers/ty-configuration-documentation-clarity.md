---
title: Configuration documentation clarity
description: Configuration documentation should be precise, specific, and include
  helpful context for users. Avoid vague or ambiguous language that could lead to
  misunderstanding of how settings behave.
repository: astral-sh/ty
label: Configurations
language: Markdown
comments_count: 10
repository_stars: 11919
---

Configuration documentation should be precise, specific, and include helpful context for users. Avoid vague or ambiguous language that could lead to misunderstanding of how settings behave.

Key principles:
- Use specific, descriptive language rather than generic terms
- Explain edge cases and special behaviors explicitly
- Include examples that illustrate the actual behavior
- Add context for beginners who may not be familiar with concepts
- Clarify when behavior differs from user expectations

For example, instead of writing:
```
Paths passed explicitly are checked even if they are otherwise ignored by an exclude or ignore file.
```

Write:
```
Paths that are passed as positional arguments to `ty check` are included even if they would otherwise be ignored through `exclude` filters or an ignore-file.
```

Similarly, when explaining pattern matching behavior, be explicit about anchoring:
```
Include patterns are anchored: The pattern `src` only includes `<project_root>/src` but not something like `<project_root>/test/src`. To include any directory named `src`, use the `**/src` prefix match.
```

This approach helps users understand exactly how configuration options will behave in their specific use cases and reduces confusion about expected vs. actual behavior.