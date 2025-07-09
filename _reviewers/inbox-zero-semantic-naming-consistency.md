---
title: Semantic naming consistency
description: 'Ensure all model and field names semantically reflect their actual purpose
  and maintain consistency with their usage throughout the codebase:


  1. Choose names that accurately represent the entity''s role without misleading
  prefixes.'
repository: elie222/inbox-zero
label: Naming Conventions
language: Prisma
comments_count: 2
repository_stars: 8267
---

Ensure all model and field names semantically reflect their actual purpose and maintain consistency with their usage throughout the codebase:

1. Choose names that accurately represent the entity's role without misleading prefixes.
2. Verify correct spelling in all identifiers.
3. Ensure data types match the documented usage patterns.

**Example:**
```diff
// Misleading model name with inappropriate type
- model UserFrequency {
-   timeOfDay DateTime?  // Comment says only time portion used
-   lastOcurrenceAt DateTime?  // Spelling error
- }

// Improved semantic naming and type consistency
+ model Schedule {
+   timeOfDay String?  // Stores time in "HH:mm" format as documented
+   lastOccurrenceAt DateTime?  // Correct spelling
+ }
```

This standard helps prevent confusion, improves code readability, and reduces the cognitive load for developers working with your schema.