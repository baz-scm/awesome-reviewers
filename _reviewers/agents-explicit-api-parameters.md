---
title: Explicit API parameters
description: Design APIs with explicit parameters rather than implicit defaults or
  hidden behavior. When an API function requires specific data or configuration, make
  those requirements clear through the function signature instead of relying on optional
  parameters with complex fallback logic.
repository: cloudflare/agents
label: API
language: TypeScript
comments_count: 3
repository_stars: 2312
---

Design APIs with explicit parameters rather than implicit defaults or hidden behavior. When an API function requires specific data or configuration, make those requirements clear through the function signature instead of relying on optional parameters with complex fallback logic.

This approach improves developer experience by making the API contract obvious and reducing confusion about what inputs are actually needed. Developers should be able to understand the API requirements without reading implementation details or documentation.

For example, instead of having optional parameters with hidden default resolution:
```typescript
// Avoid: Hidden default behavior
async function routeEmail(email: Email, env: Env, options?: {
  defaultAgentName?: string;
  defaultAgentId?: string;
}) {
  // Complex internal logic to determine routing
}

// Prefer: Explicit resolver requirement  
async function routeEmail(
  email: Email, 
  env: Env,
  resolver: EmailResolver<Env> // Required, not optional
) {
  // Clear contract - resolver is always needed
}
```

Similarly, extract and pass only the specific data needed rather than entire objects:
```typescript
// Instead of passing entire request object
const error = await doStub.onSSEMcpMessage(sessionId, request);

// Extract and pass only what's needed
const messageBody = await request.json();
const error = await doStub.onSSEMcpMessage(sessionId, messageBody);
```

This principle applies to method parameters, configuration options, and data extraction - always favor explicit, clear interfaces over implicit behavior that requires developers to understand internal implementation details.