---
title: Use descriptive consistent naming
description: Choose names that are self-explanatory, descriptive, and consistent across
  the codebase. Avoid abbreviated or informal naming that requires additional explanation.
  Follow language-specific conventions and include units or data types where appropriate.
repository: volcano-sh/volcano
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 4899
---

Choose names that are self-explanatory, descriptive, and consistent across the codebase. Avoid abbreviated or informal naming that requires additional explanation. Follow language-specific conventions and include units or data types where appropriate.

Key principles:
- Use full, descriptive names instead of abbreviations (e.g., `maximum-runtime` instead of `runsec-max`)
- Choose names that clearly indicate purpose without requiring explanation (e.g., `ReserveNodesMap` instead of `nodeForbidMap`)
- Maintain consistency across similar concepts (e.g., use `maxRetry` consistently rather than mixing `jobRetry` and `maxRetry`)
- Include units in names when relevant (e.g., `500s` instead of just `500`)
- Use proper boolean values and descriptive keys (e.g., `reserveable: true` instead of `is-reserve: 1`)
- Follow language conventions like proper capitalization and avoid keyword conflicts

Example improvements:
```yaml
# Before - informal and unclear
volcano.sh/is-reserve: 1
volcano.sh/runsec-max: 500

# After - descriptive and clear  
volcano.sh/reserveable: true
volcano.sh/maximum-runtime: 500s
```

```go
// Before - requires explanation
nodeForbidMap map[string]bool
jobRetry int

// After - self-explanatory and consistent
ReserveNodesMap map[string]bool  
maxRetry int
```