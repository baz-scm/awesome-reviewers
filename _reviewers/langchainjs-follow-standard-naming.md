---
title: Follow standard naming
description: "Use established naming patterns and correct capitalization throughout\
  \ the codebase and documentation. \n\nFor test fixtures and recordings, follow common\
  \ conventions like `__snapshots__` instead of custom directory names:"
repository: langchain-ai/langchainjs
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 15004
---

Use established naming patterns and correct capitalization throughout the codebase and documentation. 

For test fixtures and recordings, follow common conventions like `__snapshots__` instead of custom directory names:

```javascript
// Preferred
// store test recordings in __snapshots__ directory
const testData = require('./__snapshots__/test-response.json');

// Avoid
// using custom or inconsistent directory names
const testData = require('./__data__/test-response.json');
```

For product and technology names, use proper capitalization and complete names:

```markdown
// Correct
# Oracle AI Vector Search with LangChain.js Integration

// Incorrect
# Oracle Vector Search with LangchainJS Integration
```

Consistent naming improves readability, maintainability, and shows professionalism in your code and documentation.
