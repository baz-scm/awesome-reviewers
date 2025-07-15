---
title: Names reflect semantic purpose
description: Choose names that reflect the semantic purpose rather than implementation
  details or temporal characteristics. Names should be consistent across the codebase
  and accurately represent their usage.
repository: elie222/inbox-zero
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 8267
---

Choose names that reflect the semantic purpose rather than implementation details or temporal characteristics. Names should be consistent across the codebase and accurately represent their usage.

Key guidelines:
1. Use semantic names that describe the purpose rather than implementation
2. Maintain consistent naming patterns across related code
3. Ensure type/interface names accurately reflect their usage
4. Avoid encoding temporal or mutable characteristics in names

Example - Good:
```typescript
// Semantic name reflecting purpose
const labelArchiveDelayed = "label_archive_delayed";
type EmailSummaryResult = z.infer<typeof schema>;
interface Message {
  date: Date;  // Required if always needed
}
```

Example - Avoid:
```typescript
// Names tied to implementation details
const labelArchive1Week = "label_archive_1_week";
type AICheckResult = z.infer<typeof schema>;  // Misleading purpose
interface Message {
  date?: Date;  // Optional despite being required
}
```