---
title: consistent naming patterns
description: Establish and maintain consistent naming conventions across similar components
  and contexts. Inconsistent naming patterns make code harder to understand, discover,
  and maintain.
repository: novuhq/novu
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 37700
---

Establish and maintain consistent naming conventions across similar components and contexts. Inconsistent naming patterns make code harder to understand, discover, and maintain.

Key areas to focus on:
- **Path naming consistency**: Use consistent singular/plural forms in variable paths (e.g., `steps.X.eventCount` not `step.digest.eventCount`)
- **Composite identifier formats**: Follow established patterns for multi-part identifiers (e.g., `org_${orgId}:user_${userId}`)
- **Trigger and delimiter patterns**: Maintain consistent syntax for special markers and triggers across the system

Example of inconsistent naming:
```typescript
// Inconsistent - mixing singular and plural
const digestVar = 'step.digest.countSummary';  // singular 'step'
const otherVar = 'steps.workflow.events';      // plural 'steps'

// Consistent approach
const digestVar = 'steps.digest.countSummary'; // plural 'steps'
const otherVar = 'steps.workflow.events';      // plural 'steps'
```

Before introducing new naming patterns, verify they don't conflict with existing validation rules or system constraints, and ensure they follow the established conventions in similar contexts.