---
title: "Type-safe API interfaces design"
description: "Design API interfaces with strong type safety while maintaining excellent developer experience. Prefer explicit types over loose ones to enable better IDE support and catch errors at compile time."
repository: "axios/axios"
label: "API"
language: "TypeScript"
comments_count: 5
repository_stars: 107000
---

Design API interfaces with strong type safety while maintaining excellent developer experience. Prefer explicit types over loose ones to enable better IDE support and catch errors at compile time.

Key principles:
1. Use explicit generic parameters with meaningful names
2. Prefer `unknown` over `any` for better type safety
3. Use intersection types when combining interface properties
4. Avoid string literals when specific types are available

Example:
```typescript
// ❌ Avoid
interface ApiConfig {
  headers?: Record<string, any>;
  data?: any;
}

// ✅ Better
interface ApiConfig<ResponseData = unknown, RequestData = unknown> {
  headers?: HeadersDefaults & RequestHeaders;
  data?: RequestData;
  response?: AxiosResponse<ResponseData>;
}
```

This approach provides better IDE autocompletion, makes the code more maintainable, and catches potential type errors during development rather than at runtime.