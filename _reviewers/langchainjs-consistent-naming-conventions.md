---
title: Consistent naming conventions
description: 'Maintain consistent and explicit naming conventions across your codebase
  that reflect:


  1. **Component dependencies**: Class/function names should explicitly indicate their
  external dependencies and integrations to improve clarity and avoid confusion.'
repository: langchain-ai/langchainjs
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 15004
---

Maintain consistent and explicit naming conventions across your codebase that reflect:

1. **Component dependencies**: Class/function names should explicitly indicate their external dependencies and integrations to improve clarity and avoid confusion.
   ```typescript
   // INCORRECT: Doesn't indicate dependency on Unstructured API
   class DropboxLoader { ... }
   
   // CORRECT: Explicitly indicates dependency
   class DropboxUnstructuredLoader { ... }
   ```

2. **Current parameter naming**: Use the current preferred parameter names rather than deprecated ones, and be consistent across all instances.
   ```javascript
   // INCORRECT: Using deprecated parameter name
   const model = new ChatOpenAI({
     modelName: "gpt-azure",
   });
   
   // CORRECT: Using current parameter name
   const model = new ChatOpenAI({
     model: "gpt-azure",
   });
   ```

3. **Standard formatting patterns**: Follow standard naming patterns for environment variables and configuration parameters, with proper word separation.
   ```javascript
   // INCORRECT: Concatenated words without separation
   process.env.GOOGLE_DRIVE_CREDENTIALSPATH
   
   // CORRECT: Words properly separated with underscores
   process.env.GOOGLE_DRIVE_CREDENTIALS_PATH
   ```

This consistent approach to naming makes your code more maintainable, reduces confusion for other developers, and provides better clarity about component dependencies and behavior.
