---
title: Follow established naming patterns
description: Ensure all identifiers, file references, and generated names follow established
  conventions and patterns rather than using arbitrary or hardcoded values. This includes
  using correct file extensions in imports, following consistent naming patterns for
  generated targets, and using template variables instead of hardcoded names in templates.
repository: nrwl/nx
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 27518
---

Ensure all identifiers, file references, and generated names follow established conventions and patterns rather than using arbitrary or hardcoded values. This includes using correct file extensions in imports, following consistent naming patterns for generated targets, and using template variables instead of hardcoded names in templates.

Key practices:
- Follow established patterns for generated names (e.g., `ciTargetName--merge-reports` with double dashes)
- Use technically correct file extensions in import statements (`.mts` vs `.mjs`)
- Use template variables instead of hardcoded identifiers in code generation

Example violations and fixes:
```typescript
// ❌ Wrong: Single dash instead of established double-dash pattern
e2e-ci-merge-reports

// ✅ Correct: Follow the established pattern with double dashes  
e2e-ci--merge-reports

// ❌ Wrong: Hardcoded name in template
import { rule, RULE_NAME } from './my-custom-rule';

// ✅ Correct: Use template variable
import { rule, RULE_NAME } from './<%= name %>';
```

This ensures consistency across the codebase and prevents confusion when names don't follow expected patterns.