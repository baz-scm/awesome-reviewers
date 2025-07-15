---
title: "Robust Axios Usage in TypeScript"
description: "This review focuses on ensuring robust and type-safe usage of the Axios library in TypeScript codebases. Key recommendations include leveraging Axios' built-in type-checking utilities, properly handling Content-Type headers when sending data, and standardizing serialization patterns for complex data types."
repository: "axios/axios"
label: "Axios"
language: "TypeScript"
comments_count: 4
repository_stars: 107000
---

This review focuses on ensuring robust and type-safe usage of the Axios library in TypeScript codebases. Key recommendations:

1. Leverage Axios' built-in type-checking utilities rather than relying on error-prone `instanceof` checks. Use `axios.isCancel()` to detect canceled requests instead of manual type checking.

2. Properly handle Content-Type headers when sending data. Document how Axios automatically manages Content-Type for different data types (e.g. JSON, form data, URL-encoded). Provide clear examples of correct data transformation before sending, such as using `URLSearchParams` for URL-encoded form data.

3. Standardize serialization patterns for complex data types like `FormData` and nested objects to ensure consistent data handling across the codebase.

Following these practices will help ensure your Axios-based APIs remain robust and maintainable when used in applications with varying dependency versions, environments (browser/Node.js), and data formats.