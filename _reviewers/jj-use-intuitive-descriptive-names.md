---
title: Use intuitive descriptive names
description: Choose names that clearly communicate purpose and intent without requiring
  additional documentation or context. Names should be self-explanatory to users who
  encounter them for the first time.
repository: jj-vcs/jj
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 21171
---

Choose names that clearly communicate purpose and intent without requiring additional documentation or context. Names should be self-explanatory to users who encounter them for the first time.

For commands and functions, prefer descriptive verbs that indicate the action being performed. Instead of cryptic or technical references, use names that directly describe what the operation does:

```
// Poor: Unclear what "touch" does
jj touch

// Better: Clear action and target
jj metaedit
jj modify
```

For files and assets, include context about their purpose and location:

```
// Poor: Generic placement
docs/favicon.png

// Better: Organized with clear purpose
docs/images/favicon.png
docs/images/jj-logo.jpg
```

For types and data structures, avoid introducing similar names that could cause confusion. If creating new types that serve similar purposes to existing ones, either reuse the existing type or clearly deprecate the old one to maintain consistency.

This approach reduces cognitive load for developers and users, making the codebase more maintainable and intuitive to navigate.