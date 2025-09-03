---
title: Enforce permission-based UI controls
description: Always implement proper authorization checks in UI components that expose
  sensitive functionality. Wrap buttons, forms, and other interactive elements that
  perform create, update, delete, or other privileged operations with permission-based
  controls to prevent unauthorized access.
repository: novuhq/novu
label: Security
language: TSX
comments_count: 1
repository_stars: 37700
---

Always implement proper authorization checks in UI components that expose sensitive functionality. Wrap buttons, forms, and other interactive elements that perform create, update, delete, or other privileged operations with permission-based controls to prevent unauthorized access.

Use permission wrapper components or conditional rendering based on user roles/permissions to ensure that only authorized users can see and interact with sensitive functionality. This prevents both accidental and malicious access to restricted operations.

Example implementation:
```tsx
<PermissionButton
  permission={PermissionsEnum.WORKFLOW_WRITE}
  // ... other props
>
  Create Layout
</PermissionButton>
```

This pattern should be consistently applied to all UI elements that trigger sensitive operations like creating, deleting, duplicating, or modifying critical resources. The authorization check should happen both at the UI level (for user experience) and at the API level (for security enforcement).