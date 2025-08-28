---
title: Informative error messages
description: Error messages should provide specific context and actionable guidance
  to help developers understand and resolve issues effectively. Include relevant identifiers
  (class names, file paths, method names) and clear recovery instructions when possible.
repository: cloudflare/workers-sdk
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 3379
---

Error messages should provide specific context and actionable guidance to help developers understand and resolve issues effectively. Include relevant identifiers (class names, file paths, method names) and clear recovery instructions when possible.

Key practices:
- Add contextual identifiers to error messages for better debugging (e.g., include class name and method: `Cannot access "MyDurableObject#ping"`)
- Provide specific, actionable guidance rather than generic error descriptions
- Include recovery information when operations can be resumed (e.g., "assets already uploaded have been saved, so the next attempt will automatically resume")
- Ensure error attribution is correct - clearly identify which component or rule is causing the issue
- Validate critical data and throw explicit errors rather than proceeding with invalid state

Example:
```typescript
// Poor: Generic error without context
throw new Error("Upload failed");

// Better: Specific context and recovery guidance
throw new FatalError(
  `Asset upload took too long on bucket ${bucketIndex + 1}/${totalBuckets}. ` +
  `Please try again - assets already uploaded have been saved, so the next attempt will automatically resume from this point.`
);
```

This approach reduces debugging time and improves the developer experience by making failures self-explanatory and recoverable.