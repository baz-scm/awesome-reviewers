---
title: Maintain documentation consistency
description: Ensure consistent terminology, precise language, and uniform formatting
  throughout all documentation to improve clarity and user experience. Use standardized
  terms consistently (e.g., "V1" and "V2" not "v1" and "v2"), choose precise wording
  that clearly conveys intent, and maintain consistent formatting patterns.
repository: docker/compose
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 35858
---

Ensure consistent terminology, precise language, and uniform formatting throughout all documentation to improve clarity and user experience. Use standardized terms consistently (e.g., "V1" and "V2" not "v1" and "v2"), choose precise wording that clearly conveys intent, and maintain consistent formatting patterns.

Key practices:
- Use generic, future-proof terminology (e.g., "base branch" instead of specific branch names like "master")
- Choose precise language that avoids ambiguity (e.g., "Include code comments" rather than "Comment on the code" which could imply GitHub comments)
- Maintain consistent capitalization and formatting for technical terms
- Structure content with proper paragraph separation for better readability

Example of consistent terminology:
```markdown
# Good
Pull requests must be cleanly rebased on top of the base branch without multiple branches

# Avoid  
Pull requests must be cleanly rebased on top of master without multiple branches
```

Example of precise language:
```markdown
# Good
4. Include code comments. Tell us the why, the history and the context.

# Avoid
4. Comment on the code. Tell us the why, the history and the context.
```

This consistency reduces confusion, improves maintainability, and creates a more professional user experience across all documentation.