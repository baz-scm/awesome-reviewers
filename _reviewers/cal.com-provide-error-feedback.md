---
title: Provide error feedback
description: Always provide clear user feedback when errors occur or operations fail,
  rather than allowing silent failures or showing disabled UI without explanation.
  This includes detecting existing error states, preventing validation errors through
  input sanitization, and displaying appropriate messages for failed operations.
repository: calcom/cal.com
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 37732
---

Always provide clear user feedback when errors occur or operations fail, rather than allowing silent failures or showing disabled UI without explanation. This includes detecting existing error states, preventing validation errors through input sanitization, and displaying appropriate messages for failed operations.

Key practices:
- Replace silent failures with explicit error detection and user messaging
- Show warning messages instead of unexplained disabled UI elements  
- Provide toast notifications for operations that can fail
- Sanitize inputs to prevent downstream validation errors
- Clear problematic form state proactively to avoid validation conflicts

Example from the discussions:
```tsx
// Bad: Silent failure with disabled select
<Select isDisabled={isPending} />

// Good: Clear messaging about why functionality is unavailable  
{!userHasDefaultSchedule ? (
  <Alert severity="warning" title={t("view_only_edit_availability_not_onboarded")} />
) : (
  <Select isDisabled={isPending} />
)}
```

This prevents user confusion and ensures they understand why certain actions are unavailable or have failed.