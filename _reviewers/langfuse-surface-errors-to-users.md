---
title: Surface errors to users
description: 'Always provide user-visible feedback for errors instead of only logging
  to the console. This ensures users are aware of failures and can take appropriate
  action. This is especially important for:'
repository: langfuse/langfuse
label: Error Handling
language: TSX
comments_count: 7
repository_stars: 13574
---

Always provide user-visible feedback for errors instead of only logging to the console. This ensures users are aware of failures and can take appropriate action. This is especially important for:
- API/mutation failures
- Async operations
- Form validations
- User interactions

Example converting console-only error to user feedback:

```typescript
// Before
const handleAction = async () => {
  try {
    await someAsyncOperation();
  } catch (err) {
    console.error(err); // Silent failure
  }
};

// After
const handleAction = async () => {
  try {
    await someAsyncOperation();
  } catch (err) {
    console.error(err);
    showErrorToast("Operation failed", err.message);
    // or
    setError("Failed to complete action. Please try again.");
  }
};
```

For mutations, implement both success and error handlers:

```typescript
const mutation = api.something.mutate.useMutation({
  onSuccess: () => {
    showSuccessToast("Operation completed");
    // Update UI state
  },
  onError: (e) => {
    showErrorToast("Operation failed", e.message);
    // Preserve UI state
  }
});
```