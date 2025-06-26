---
title: "Maintain Consistent Naming Conventions in Next.js Code"
description: "As a code reviewer for Next.js projects, ensure that all code artifacts, including component names, file names, and configuration keys, adhere to consistent naming conventions."
repository: "vercel/next.js"
label: "Next.js"
language: "JavaScript"
comments_count: 4
repository_stars: 133000
---

As a code reviewer for Next.js projects, ensure that all code artifacts, including component names, file names, and configuration keys, adhere to consistent naming conventions. This helps improve code readability, maintainability, and alignment with the Next.js framework's best practices.

Key guidelines:
1. Use consistent file extensions for Next.js components: `.jsx` for React components and `.js` for non-React JavaScript files.
2. Maintain case sensitivity in Next.js configuration keys and API parameters, such as `staticPageGenerationSourcemaps` instead of `staticPageGenerationSourceMaps`.
3. Choose clear, concise, and consistent terminology for Next.js-specific concepts, such as "pages", "components", "middleware", and "API routes".

Example of inconsistent Next.js code:
```javascript
// Inconsistent file extensions
pages/search.js   // Should be search.jsx for a React component
pages/utils.ts   // Should be utils.js for a non-React JavaScript file

// Inconsistent configuration keys
next.config.js:
{
  staticPageGenerationSourceMaps: false, // Documentation
  staticPageGenerationSourcemaps: false // Implementation
}
```

Corrected version:
```javascript
// Consistent file extensions
pages/search.jsx  // React component
pages/utils.js    // Non-React JavaScript file

// Consistent configuration keys
next.config.js:
{
  staticPageGenerationSourcemaps: false, // Matches implementation
}
```