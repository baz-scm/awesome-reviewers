---
title: Format AI code identifiers
description: When documenting AI systems, always format code identifiers, function
  names, agent names, model names, and other technical references with backticks (`)
  to improve readability and clearly distinguish them from regular text. This is particularly
  important in AI documentation where specialized components like agents, models,
  and functions need to be visually...
repository: prowler-cloud/prowler
label: AI
language: Markdown
comments_count: 2
repository_stars: 11834
---

When documenting AI systems, always format code identifiers, function names, agent names, model names, and other technical references with backticks (`) to improve readability and clearly distinguish them from regular text. This is particularly important in AI documentation where specialized components like agents, models, and functions need to be visually distinct.

```markdown
// Incorrect
The overview_agent provides a summary of connected cloud accounts.

// Correct
The `overview_agent` provides a summary of connected cloud accounts.
```

This formatting practice helps developers quickly identify technical components within documentation, making it easier to understand the architecture and implementation details of AI systems. Consistent formatting of identifiers also improves searchability of documentation and reduces confusion when discussing specific system components.