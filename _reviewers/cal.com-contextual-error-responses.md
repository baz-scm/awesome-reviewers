---
title: Contextual error responses
description: Choose error response strategies based on the error's origin, caller
  context, and downstream impact rather than blindly propagating upstream errors.
  Consider whether throwing a 5xx error will cause harmful retries or mislead about
  the actual source of the problem.
repository: calcom/cal.com
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 37732
---

Choose error response strategies based on the error's origin, caller context, and downstream impact rather than blindly propagating upstream errors. Consider whether throwing a 5xx error will cause harmful retries or mislead about the actual source of the problem.

For external webhooks and integrations, return 2xx responses with error details in the response body to prevent retry storms when the issue is internal misconfiguration:

```typescript
// Instead of throwing 500 for internal config issues
if (!webhookToken) {
  throw new HttpError({ statusCode: 500, message: "Token not configured" });
}

// Return 200 with error details to prevent retries
if (!webhookToken) {
  return {
    message: "ok",
    processed: 0,
    failed: 0,
    skipped: payload.value.length,
    errors: ["MICROSOFT_WEBHOOK_TOKEN is not defined"],
  };
}
```

For user input validation errors, use 4xx status codes even when the error originates from a downstream service:

```typescript
// If Twilio returns 400 for invalid phone number user entered
if (isTwilioError(cause) && cause.status === 400) {
  return new HttpError({ statusCode: 400, message: cause.message });
}
```

Log upstream errors appropriately while returning status codes that accurately reflect whether the issue is with the client request, server configuration, or external service availability.