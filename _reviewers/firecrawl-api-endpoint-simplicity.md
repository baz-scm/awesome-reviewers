---
title: API endpoint simplicity
description: Design API endpoints with concise, direct naming that clearly communicates
  their purpose without unnecessary verbosity. Avoid redundant prefixes or overly
  descriptive names that make endpoints harder to remember and use. Choose built-in
  language features over custom implementations when possible to improve reliability
  and maintainability.
repository: firecrawl/firecrawl
label: API
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Design API endpoints with concise, direct naming that clearly communicates their purpose without unnecessary verbosity. Avoid redundant prefixes or overly descriptive names that make endpoints harder to remember and use. Choose built-in language features over custom implementations when possible to improve reliability and maintainability.

For endpoint naming, prefer the core functionality over implementation details:
```javascript
// Avoid verbose prefixes
v1Router.post("/generate-llmstxt", ...)  // ❌ Too verbose

// Prefer direct, clear naming  
v1Router.post("/llmstxt", ...)          // ✅ Concise and clear
```

For implementation, leverage built-in APIs over custom logic:
```javascript
// Avoid custom regex for URL handling
const isCompleteUrl = new RegExp('^(?:[a-z+]+:)?//', 'i');
if (!isCompleteUrl.test(link)){
  link = this.baseUrl + link;
}

// Use built-in URL constructor
const url = new URL(link.trim(), this.baseUrl);  // ✅ Simpler and more reliable
```

This approach improves developer experience by making APIs more intuitive to use and implementations easier to understand and maintain.