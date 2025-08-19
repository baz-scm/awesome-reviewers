---
title: Configuration naming clarity
description: Ensure configuration variable names, display labels, and feature flag
  names accurately reflect their actual purpose and behavior. Misleading or outdated
  names create confusion for both developers and users, making the codebase harder
  to maintain and understand.
repository: PostHog/posthog
label: Configurations
language: TSX
comments_count: 2
repository_stars: 28460
---

Ensure configuration variable names, display labels, and feature flag names accurately reflect their actual purpose and behavior. Misleading or outdated names create confusion for both developers and users, making the codebase harder to maintain and understand.

When configuration names don't match their function, it leads to situations where developers must add explanatory comments or use workarounds. For example, avoid using generic names like "New query engine" when the underlying flag is "WEB_ANALYTICS_API", and update variable names when their scope changes (like renaming MAX_SELECT_RETURNED_ROWS when it specifically applies to CSV exports).

Example of good practice:
```typescript
// Good: Name reflects actual purpose
const MAX_CSV_EXPORT_ROWS = 300000

// Bad: Generic name doesn't indicate CSV-specific usage  
const MAX_SELECT_RETURNED_ROWS = 300000
```

When introducing new features or changing existing ones, take time to review and update related configuration names to maintain clarity and prevent technical debt.