---
title: Maintain naming consistency
description: Ensure consistent terminology and naming conventions across the entire
  codebase. Use the same identifier names for the same concepts throughout all modules,
  files, and APIs. Avoid defining the same logical entity with different names in
  different places.
repository: unionlabs/union
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 74800
---

Ensure consistent terminology and naming conventions across the entire codebase. Use the same identifier names for the same concepts throughout all modules, files, and APIs. Avoid defining the same logical entity with different names in different places.

Key principles:
- Use consistent terminology across all components (e.g., consistently use "receiver" instead of mixing "receiver" and "recipient")
- Follow established protocol or framework naming standards (e.g., use "ucs01-relay-1" format for version identifiers)
- Maintain single source of truth for variable definitions - avoid defining the same concept in multiple places with different names
- When renaming for consistency, update all related code simultaneously

Example of inconsistent naming to avoid:
```typescript
// Bad: Same concept with different names
const recipient = $page.url.searchParams.get("receiver") 
const transferHash = await unionClient.transferAsset({
  recipient: $recipient  // Should be "receiver" to match URL param
})

// Good: Consistent naming
const receiver = $page.url.searchParams.get("receiver")
const transferHash = await unionClient.transferAsset({
  receiver: $receiver
})
```

This prevents confusion, reduces cognitive load, and makes the codebase more maintainable by ensuring developers can rely on consistent naming patterns.