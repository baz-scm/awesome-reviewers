---
title: AI dependency management
description: 'When integrating AI models and language processing libraries, follow
  these dependency management best practices:


  1. Use specific model integration packages instead of general-purpose AI SDKs. For
  example:'
repository: langchain-ai/langchainjs
label: AI
language: Json
comments_count: 3
repository_stars: 15004
---

When integrating AI models and language processing libraries, follow these dependency management best practices:

1. Use specific model integration packages instead of general-purpose AI SDKs. For example:
```javascript
// AVOID direct dependencies like this:
// "dependencies": {
//   "openai": "^4.72.0"
// }

// RECOMMENDED: Use model-specific packages
// Install with: npm install @langchain/openai
// "dependencies": {
//   "@langchain/openai": "^x.x.x"
// }
```

2. Don't include AI service libraries as hard dependencies. Follow project contribution guidelines for integrations by making them optional or peer dependencies.

3. When updating AI SDK versions, clearly flag these changes for maintainers to review, as they may impact compatibility or introduce new features that require additional testing.

This approach ensures better maintainability, clearer dependency trees, and more explicit relationships between your project and the AI services it leverages.
