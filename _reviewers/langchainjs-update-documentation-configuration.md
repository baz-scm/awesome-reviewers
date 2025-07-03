---
title: Update documentation configuration
description: When adding new files or components to the project, ensure that documentation
  configuration is updated accordingly. This includes adding new files to TypeDoc
  options in tsconfig.json to maintain complete API documentation coverage. Additionally,
  clearly mark deprecated components and direct developers to use the recommended
  alternatives instead of extending...
repository: langchain-ai/langchainjs
label: Documentation
language: Json
comments_count: 2
repository_stars: 15004
---

When adding new files or components to the project, ensure that documentation configuration is updated accordingly. This includes adding new files to TypeDoc options in tsconfig.json to maintain complete API documentation coverage. Additionally, clearly mark deprecated components and direct developers to use the recommended alternatives instead of extending deprecated functionality.

Example:
```javascript
// When adding a new file like document_loaders/fs/md.ts
// Remember to update the TypeDoc configuration in tsconfig.json:

"typedocOptions": {
  "entryPoints": [
    // existing entries
    "document_loaders/fs/md.ts"
  ]
}

// For deprecated components, add clear documentation:
/**
 * @deprecated This entrypoint is deprecated. 
 * Please use the community integration instead.
 */
```

This practice ensures comprehensive documentation coverage and provides clear guidance for developers, preventing them from extending deprecated features and helping them locate the proper integration points for new functionality.
