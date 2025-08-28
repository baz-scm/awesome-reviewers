---
title: Consider semantic context
description: When choosing names for variables, methods, classes, or configuration
  sections, consider both the current purpose and potential future extensions. Names
  should be semantically accurate and align with established conventions in the codebase.
repository: kilo-org/kilocode
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 7302
---

When choosing names for variables, methods, classes, or configuration sections, consider both the current purpose and potential future extensions. Names should be semantically accurate and align with established conventions in the codebase.

For configuration sections or groupings, choose names that can accommodate related functionality rather than being overly specific. For example, prefer "triggers" over "keybindings" if the section might later include other trigger types like diagnostics or watch triggers.

Always verify that naming choices follow existing team conventions and documented rules. Consistency with established patterns is crucial for maintainability.

Example:
```json
// Instead of overly specific:
"keybindings": { ... }

// Choose semantically broader:
"triggers": { 
  "keybindings": { ... },
  // Future: "diagnostics": { ... }
}
```