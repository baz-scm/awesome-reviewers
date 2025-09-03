---
title: eliminate code duplication
description: Identify and eliminate duplicated code by extracting shared functionality
  to appropriate locations. When multiple components or code sections perform identical
  operations, consolidate the logic into a single, reusable location such as a parent
  component, utility function, or shared module.
repository: langflow-ai/langflow
label: Code Style
language: TSX
comments_count: 3
repository_stars: 111046
---

Identify and eliminate duplicated code by extracting shared functionality to appropriate locations. When multiple components or code sections perform identical operations, consolidate the logic into a single, reusable location such as a parent component, utility function, or shared module.

Key strategies:
- Move shared functionality to parent components when child components perform identical operations
- Extract duplicated logic into utility functions or helper methods
- Break down large components to better identify and organize shared code patterns

Example of eliminating platform duplication:
```typescript
// Before: Duplicated code for different platforms
if (detectedPlatform === "powershell") {
  const authHeader = ` -H "x-api-key: YOUR_API_KEY_HERE"`;
  uploadCommands.push(`curl -X POST "${baseUrl}/api/v1/files/upload/${flowId}"${authHeader} -F "file=@your_image.jpg"`);
} else {
  const authHeader = ` -H "x-api-key: YOUR_API_KEY_HERE"`;
  uploadCommands.push(`curl -X POST "${baseUrl}/api/v1/files/upload/${flowId}"${authHeader} -F "file=@your_image.jpg"`);
}

// After: Extracted shared logic
const authHeader = ` -H "x-api-key: YOUR_API_KEY_HERE"`;
uploadCommands.push(`curl -X POST "${baseUrl}/api/v1/files/upload/${flowId}"${authHeader} -F "file=@your_image.jpg"`);
```

This approach improves maintainability, reduces the likelihood of inconsistencies, and makes the codebase more readable by eliminating redundant patterns.