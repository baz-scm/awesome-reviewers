---
title: Simplify code organization
description: 'Maintain clean code organization by eliminating unnecessary abstractions
  and preventing codebase fragmentation. This applies both at the component level
  and module level:'
repository: langchain-ai/langchainjs
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 15004
---

Maintain clean code organization by eliminating unnecessary abstractions and preventing codebase fragmentation. This applies both at the component level and module level:

1. Avoid creating wrapper components that don't add functionality
   ```jsx
   // Don't do this:
   function InstallationInfo({ children }) {
     return <Npm2Yarn>{children}</Npm2Yarn>;
   }
   
   // Do this instead:
   <Npm2Yarn>{content}</Npm2Yarn>
   ```

2. Consolidate related functionality into logical groups rather than creating new isolated entry points:
   ```js
   // Don't do this:
   "utils/is_openai_tool": "utils/is_openai_tool",
   
   // Do this instead:
   // Add to existing related module like "language_models/base"
   ```

This approach reduces code complexity, improves maintainability, and makes the codebase easier to navigate and understand.
