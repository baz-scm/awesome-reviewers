---
title: Abstract user-facing errors
description: Error messages displayed to end users should abstract away implementation
  details while providing actionable information. Avoid exposing internal system components
  (like "containerd", "K8S") or raw error messages that might confuse users or reveal
  security-sensitive information. Instead, map technical errors to user-friendly messages
  that explain what...
repository: supabase/supabase
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 86070
---

Error messages displayed to end users should abstract away implementation details while providing actionable information. Avoid exposing internal system components (like "containerd", "K8S") or raw error messages that might confuse users or reveal security-sensitive information. Instead, map technical errors to user-friendly messages that explain what happened and suggest possible next steps.

Always implement proper validation and error handling for data from external sources by using try-catch blocks, and ensure error information is properly displayed regardless of how it's transmitted (URL parameters, hash fragments, etc.).

For example, instead of:
```typescript
// DON'T do this - exposes implementation details
if (failedStatus.message?.startsWith('unable to retrieve container logs for containerd://')) {
  // show loading state
}
```

Do this:
```typescript
// Abstract error details with a function
function isTransientLogLoadingError(message: string): boolean {
  // Check for known transient errors without exposing details to UI
  return message?.includes('retrieve container logs') || message?.includes('logs unavailable');
}

try {
  // Attempt to display logs
  if (isTransientLogLoadingError(failedStatus.message)) {
    return <LoadingState message="Logs are still loading..." />;
  } else {
    return <ErrorState message="Unable to load logs. Please try again later." />;
  }
} catch (error) {
  // Fallback for any unexpected errors
  return <ErrorState message="Something went wrong. Please try again." />;
}
```