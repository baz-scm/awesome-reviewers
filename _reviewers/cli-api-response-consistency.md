---
title: API response consistency
description: Ensure consistent patterns for API response handling, error management,
  and type safety across all API interactions. This includes standardizing error response
  structures based on status codes, properly defining response types to match actual
  API behavior, and implementing robust error handling with appropriate fallbacks.
repository: snyk/cli
label: API
language: TypeScript
comments_count: 7
repository_stars: 5178
---

Ensure consistent patterns for API response handling, error management, and type safety across all API interactions. This includes standardizing error response structures based on status codes, properly defining response types to match actual API behavior, and implementing robust error handling with appropriate fallbacks.

Key principles:
1. **Status-specific error handling**: Different HTTP status codes should have consistent response body handling (e.g., 400 errors with JSON bodies vs 401/403 with string responses)
2. **Type accuracy**: Response types should reflect actual API behavior, including union types when fields can have multiple formats
3. **Proper HTTP response patterns**: Always return after sending responses to prevent multiple response attempts
4. **Structured response access**: Use consistent patterns for accessing nested API response data
5. **Timeout and retry logic**: Implement proper polling mechanisms with clear timeout handling

Example of consistent error handling:
```typescript
if (res.statusCode === 400) {
  return reject({
    code: res.statusCode,
    body: JSON.parse(body as any), // JSON response for user feedback
  });
} else if (res.statusCode >= 401) {
  return reject({
    code: res.statusCode,
    // No body parsing for non-JSON responses
  });
}
```

Example of proper response type definition:
```typescript
interface ApiResponse {
  remediation: string | { resolve: string }; // Union type reflecting actual API behavior
  target?: GitTarget | ContainerTarget | {}; // Optional with fallback
}
```

This ensures APIs are predictable, type-safe, and handle edge cases gracefully while maintaining consistency across different endpoints and response scenarios.