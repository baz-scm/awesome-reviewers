---
title: Provide specific error context
description: Error messages should be specific and contextual rather than generic,
  helping users understand exactly what went wrong and where. When handling errors,
  provide detailed information about the cause and set errors on the specific fields
  or components that triggered them.
repository: novuhq/novu
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 37700
---

Error messages should be specific and contextual rather than generic, helping users understand exactly what went wrong and where. When handling errors, provide detailed information about the cause and set errors on the specific fields or components that triggered them.

For API errors, catch specific error conditions and set targeted error messages:

```typescript
onError: (error) => {
  // Check if it's a conflict error (topic already exists)
  if (error instanceof NovuApiError && error.status === 409) {
    // Set error on the key field specifically
    form.setError('key', {
      type: 'manual',
      message: 'A topic with this key already exists',
    });
  }
}
```

Instead of generic messages like "Step was skipped", provide context about why the action failed: "Step skipped due to missing credentials" or "Step skipped - email address required". This helps users quickly understand what happened and what they might need to do to resolve the issue.