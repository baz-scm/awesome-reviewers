---
title: Follow consistent semantic naming
description: Ensure that names accurately reflect their purpose and maintain consistency
  with established patterns in the codebase. Method names should clearly indicate
  their behavior - avoid misleading conventions when they don't match the actual functionality.
  Similarly, maintain consistent naming patterns across similar contexts.
repository: kilo-org/kilocode
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 7302
---

Ensure that names accurately reflect their purpose and maintain consistency with established patterns in the codebase. Method names should clearly indicate their behavior - avoid misleading conventions when they don't match the actual functionality. Similarly, maintain consistent naming patterns across similar contexts.

For example, avoid using "set" prefixes for methods that don't actually set a value:
```typescript
// Misleading - implies setting a value
setNotificationDismissed: (notificationId: string) => void

// Clear - accurately describes the action
markNotificationAsDismissed: (notificationId: string) => void
```

Also ensure consistency in organizational naming patterns:
```typescript
// Inconsistent
title: "UI/Badge"     // in Badge.stories.tsx
title: "Component/Button"  // in Button.stories.tsx

// Consistent
title: "Component/Badge"   // matches established pattern
title: "Component/Button"
```

This approach helps maintain code readability and reduces confusion for team members working across different parts of the codebase.