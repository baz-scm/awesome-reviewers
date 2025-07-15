---
title: "Consistent Naming Conventions for Axios Requests and Responses"
description: "When using the Axios library in TypeScript, it is important to follow consistent naming conventions to improve code readability and maintainability. Use the 'on' prefix for Axios event handlers and callbacks, use domain-specific prefixes like 'response' to clarify scope, maintain consistent naming patterns for similar functionality, and align with established conventions."
repository: "axios/axios"
label: "Axios"
language: "TypeScript"
comments_count: 3
repository_stars: 107000
---

When using the Axios library in TypeScript, it is important to follow consistent naming conventions to improve code readability and maintainability. Specifically:

1. Use the "on" prefix for Axios event handlers and callbacks, such as `onUploadProgress` and `onDownloadProgress`.
2. Use domain-specific prefixes like "response" to clarify the scope of Axios-related functionality, such as `responseEncoding` and `responseType`.
3. Maintain consistent naming patterns for similar Axios-related functionality, such as using the same parameter structure for authentication-related properties.
4. Align Axios-specific naming with established conventions in the TypeScript ecosystem, such as using camelCase for properties and methods.

Following these practices will help developers working on your Axios-based code understand the purpose and usage of your API more intuitively. Provide clear, well-named Axios-related functionality to improve the developer experience.

Example:
```typescript
// ✅ Good - Clear event handler naming with "on" prefix
const config: AxiosRequestConfig = {
  onUploadProgress: (progressEvent: ProgressEvent) => { /* ... */ },
  onDownloadProgress: (progressEvent: ProgressEvent) => { /* ... */ }
}

// ❌ Bad - Unclear purpose of the function
const config: AxiosRequestConfig = {
  uploadProgress: (progressEvent: ProgressEvent) => { /* ... */ },
  downloadProgress: (progressEvent: ProgressEvent) => { /* ... */ }
}

// ✅ Good - Consistent parameter structure and clear scope
const config: AxiosRequestConfig = {
  responseEncoding: 'utf-8',
  proxy: {
    auth: { username: 'mikeymike', password: 'rapunz3l' } // Matches other auth patterns
  }
}
```