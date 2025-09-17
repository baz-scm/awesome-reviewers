---
title: Documentation language precision
description: Ensure documentation uses precise, accurate language that clearly describes
  functionality and highlights important behaviors users need to understand. Avoid
  vague or misleading terms that could confuse users about what the code actually
  does.
repository: microsoft/markitdown
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 76602
---

Ensure documentation uses precise, accurate language that clearly describes functionality and highlights important behaviors users need to understand. Avoid vague or misleading terms that could confuse users about what the code actually does.

Key practices:
- Use specific, accurate verbs (e.g., "shows how to" instead of "allows you to" when describing examples)
- Explicitly state important behaviors and side effects (e.g., "original files remain unchanged")
- Tailor language to the documentation's specific purpose and audience
- Avoid unnecessary duplication while maintaining completeness where needed

Example improvement:
```markdown
// Instead of:
"This extension allows you to convert multiple files..."

// Use:
"This example shows how to convert multiple files..."

// And add clarifying details:
"Note that original files will remain unchanged and new markdown files are created with the same base name."
```

This ensures users have accurate expectations about functionality and understand important implementation details that affect their workflow.