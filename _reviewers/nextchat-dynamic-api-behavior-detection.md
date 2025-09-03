---
title: Dynamic API behavior detection
description: APIs should determine behavior based on runtime request characteristics
  rather than static configuration flags. This enables multiple API providers and
  models to coexist and ensures proper handling of provider-specific requirements.
repository: ChatGPTNextWeb/NextChat
label: API
language: TypeScript
comments_count: 4
repository_stars: 85721
---

APIs should determine behavior based on runtime request characteristics rather than static configuration flags. This enables multiple API providers and models to coexist and ensures proper handling of provider-specific requirements.

Instead of using static configuration flags, inspect the actual request to determine the appropriate behavior:

```typescript
// ❌ Avoid: Static configuration-based decisions
if (serverConfig.isAzure) {
  // Azure-specific logic
}

// ✅ Prefer: Runtime request-based decisions  
if (req.nextUrl.pathname.includes("azure/deployments")) {
  // Azure-specific logic detected from request path
}

// ❌ Avoid: Model name-based assumptions
if (!chatPath.includes("gemini-pro")) {
  // Logic based on model name
}

// ✅ Prefer: Functionality-based detection
if (shouldUseStreamMode(request)) {
  // Logic based on actual streaming requirement
}
```

This approach allows for more flexible API routing, enables multiple providers to work simultaneously, and makes the system more maintainable by reducing coupling between configuration and runtime behavior. Always inspect request paths, parameters, and headers to make informed decisions about API behavior rather than relying on global flags.