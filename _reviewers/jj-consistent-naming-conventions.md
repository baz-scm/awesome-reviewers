---
title: Consistent naming conventions
description: Maintain consistent naming and terminology throughout code and documentation.
  This includes proper capitalization of product names, technical terms, and consistent
  use of domain-specific vocabulary.
repository: jj-vcs/jj
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 21171
---

Maintain consistent naming and terminology throughout code and documentation. This includes proper capitalization of product names, technical terms, and consistent use of domain-specific vocabulary.

Key guidelines:
- Capitalize proper nouns consistently: "Jujutsu" not "jujutsu", "Git" not "git"
- Use consistent capitalization for technical terms: "change ID" not "change id"  
- Apply consistent heading formats: use sentence case for headings
- Prefer domain-specific terminology over generic terms: "revisions" instead of "commits" when working with Jujutsu concepts
- Choose names that fit existing patterns in the codebase: if you have `jj revert`, use `jj op revert` for consistency
- Avoid overloaded terms that have different meanings in other systems

Example corrections:
```markdown
# Before
### Commit Evolution (Change-IDs and Changes)
amend or rewrite your commits
change id

# After  
### Commit evolution (change IDs and changes)
update your revisions
change ID
```

This ensures users can easily understand and predict naming patterns, reducing cognitive load and improving overall code/documentation quality.