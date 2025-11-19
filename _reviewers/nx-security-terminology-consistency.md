---
title: Security terminology consistency
description: Ensure consistent formatting and precise terminology when documenting
  security-related concepts, access controls, and system boundaries. Inconsistent
  or imprecise language in security documentation can lead to misunderstandings about
  permissions, access patterns, and security mechanisms.
repository: nrwl/nx
label: Security
language: Markdown
comments_count: 3
repository_stars: 27518
---

Ensure consistent formatting and precise terminology when documenting security-related concepts, access controls, and system boundaries. Inconsistent or imprecise language in security documentation can lead to misunderstandings about permissions, access patterns, and security mechanisms.

Key practices:
- Use consistent formatting for technical security terms (e.g., `read-write` tokens, `read-only` tokens)
- Use precise and standardized terminology for system components (e.g., "shared global cache" rather than "shared primary cache")
- Clearly describe security boundaries and access patterns to prevent misconfigurations
- Maintain consistency in how security concepts are presented across documentation

Example:
```markdown
// Inconsistent - avoid
Read-write tokens allow access to the shared primary cache.

// Consistent - preferred  
The `read-write` tokens allow full write access to your shared global cache.
```

This practice is critical for security documentation where imprecise language can lead to incorrect implementations or security vulnerabilities.