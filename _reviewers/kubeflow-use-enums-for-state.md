---
title: Use enums for state
description: When handling nullable or undefined states, use enumerations instead
  of primitive types like boolean or null/undefined. Enums provide more descriptive
  and type-safe representations of different states, including the absence of a value
  or an unknown state.
repository: kubeflow/kubeflow
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 15064
---

When handling nullable or undefined states, use enumerations instead of primitive types like boolean or null/undefined. Enums provide more descriptive and type-safe representations of different states, including the absence of a value or an unknown state.

Instead of:
```typescript
private dashboardConnectedSource = new BehaviorSubject<boolean>(true);
```

Use an enum to explicitly represent all possible states:
```typescript
enum DashboardState {
  Unknown = 0, // Initial state before connection status is determined
  Connected,
  Disconnected,
}

private dashboardStateSource = new BehaviorSubject<DashboardState>(DashboardState.Unknown);
```

This approach prevents misleading default values, improves code readability, and provides better type safety. When making decisions based on state, the enum forces you to handle all possibilities, reducing the likelihood of bugs related to unexpected null or undefined values.
