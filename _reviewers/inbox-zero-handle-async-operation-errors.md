---
title: Handle async operation errors
description: Always wrap asynchronous operations in try-catch-finally blocks to prevent
  unhandled promise rejections and ensure proper cleanup. When errors occur, provide
  users with meaningful feedback while preserving application state.
repository: elie222/inbox-zero
label: Error Handling
language: TSX
comments_count: 14
repository_stars: 8267
---

Always wrap asynchronous operations in try-catch-finally blocks to prevent unhandled promise rejections and ensure proper cleanup. When errors occur, provide users with meaningful feedback while preserving application state.

```typescript
// Before: Error-prone async operation
const handleSubmit = async () => {
  setIsSubmitting(true);
  const result = await submitData(formData);
  setIsSubmitting(false); // Never executes if submitData fails
  if (result.error) {
    showError(result.error);
    return;
  }
  navigateToSuccess();
};

// After: Robust error handling
const handleSubmit = async () => {
  setIsSubmitting(true);
  try {
    const result = await submitData(formData);
    
    if (result.error) {
      showError(result.error);
      return;
    }
    
    navigateToSuccess();
  } catch (error) {
    console.error("Submission failed:", error);
    toastError({
      title: "Failed to submit data",
      description: error instanceof Error ? error.message : "Unknown error"
    });
  } finally {
    setIsSubmitting(false); // Always executes, ensuring UI state is reset
  }
};
```

This pattern prevents common issues like:
- Unhandled promise rejections crashing the application
- Loading indicators stuck in active state after errors
- Silent failures that confuse users
- Missing error logs that make debugging difficult

For React components fetching data, also ensure error states are properly handled in the UI:

```typescript
function DataComponent() {
  const { data, error, isLoading } = useSWR('/api/data');
  
  if (error) {
    return <ErrorDisplay message="Failed to load data" />;
  }
  
  if (isLoading) {
    return <LoadingIndicator />;
  }
  
  return <DataDisplay data={data} />;
}
```