---
title: TypeScript naming standards
description: 'Follow consistent naming conventions in TypeScript to improve code clarity,
  type safety, and developer experience:


  1. **Capitalize types and interfaces**: All type and interface names should start
  with an uppercase letter.'
repository: langchain-ai/langchainjs
label: Naming Conventions
language: TypeScript
comments_count: 10
repository_stars: 15004
---

Follow consistent naming conventions in TypeScript to improve code clarity, type safety, and developer experience:

1. **Capitalize types and interfaces**: All type and interface names should start with an uppercase letter.
   ```typescript
   // Incorrect
   type chainTypeName = "stuff" | "map_reduce";
   
   // Correct
   type ChainTypeName = "stuff" | "map_reduce";
   ```

2. **Use `unknown` instead of `any`**: When the type is truly not known, prefer `unknown` over `any` for better type safety.
   ```typescript
   // Incorrect - too permissive
   function isBuiltinTool(tool: any)
   
   // Correct - safer typing
   function isBuiltinTool(tool: unknown)
   ```

3. **Prefer type literals over strings** for constrained values to improve developer experience and catch errors at compile time.
   ```typescript
   // Incorrect
   function createLoader(mode: string)
   
   // Correct
   type SearchMode = "subreddit" | "username";
   function createLoader(mode: SearchMode)
   ```

4. **Use visibility modifiers** instead of naming conventions for private/protected members:
   ```typescript
   // Incorrect
   class GraphQLClientTool {
     _endpoint: string;
   }
   
   // Correct
   class GraphQLClientTool {
     private endpoint: string;
   }
   ```

5. **Standardize parameter naming** across similar components (e.g., use `model` instead of `modelName` for consistency):
   ```typescript
   // Standardized
   interface EmbeddingsParams {
     model: string;  // Not modelName
   }
   ```

6. **Improve type precision** when appropriate to enhance developer experience:
   ```typescript
   // Less precise
   loaders: { [extension: string]: (path: string) => Loader }
   
   // More precise
   loaders: { [extension: `.${string}`]: (path: string) => Loader }
   ```
