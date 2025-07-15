---
title: "Flexible configuration design"
description: "Design configuration interfaces to be flexible and extensible rather than overly specific. When creating configuration objects, make configuration parameters optional when possible with sensible defaults and allow for arbitrary additional properties rather than creating specific fields for custom configurations."
repository: "axios/axios"
label: "Configurations"
language: "TypeScript"
comments_count: 2
repository_stars: 107000
---

Design configuration interfaces to be flexible and extensible rather than overly specific. When creating configuration objects:

1. Make configuration parameters optional when possible with sensible defaults
2. Allow for arbitrary additional properties rather than creating specific fields for custom configurations

**Example - Instead of this:**
```typescript
export interface AxiosRequestConfig<D = any> {
  // other properties...
  customConfig?: Record<string, any>;
}

// Required configuration parameter
getUri(config: AxiosRequestConfig): string;
```

**Do this:**
```typescript
export interface AxiosRequestConfig<D = any> {
  // other properties...
  [key: string]: any; // Allow arbitrary properties
}

// Optional configuration parameter
getUri(config?: AxiosRequestConfig): string;
```

This approach allows consumers to extend configurations naturally without requiring interface changes for each new use case, while maintaining backward compatibility through sensible defaults.