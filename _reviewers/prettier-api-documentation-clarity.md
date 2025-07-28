---
title: API documentation clarity
description: Ensure API documentation provides clear, accurate, and comprehensive
  information for developers. This includes precise function signatures, detailed
  parameter descriptions, correct terminology, and helpful external references.
repository: prettier/prettier
label: API
language: Markdown
comments_count: 4
repository_stars: 50772
---

Ensure API documentation provides clear, accurate, and comprehensive information for developers. This includes precise function signatures, detailed parameter descriptions, correct terminology, and helpful external references.

Key practices:
- Use accurate technical terminology (e.g., "file basename or extension" instead of vague descriptions)
- Include complete function signatures that reflect actual usage patterns
- Provide helpful context and examples for complex parameters
- Add links to relevant external documentation when referencing standard APIs
- Fix typos and grammatical errors that could confuse developers

Example of good API documentation:
```ts
// Clear function signature with proper typing
function parse(text: string, options?: ParserOptions): Promise<AST> | AST;

// Detailed parameter description with examples
// The `file` parameter could be a normal path or a url string like `file:///C:/test.txt`

// Helpful external reference
Strings provided to `plugins` are ultimately passed to [`import()` expression](https://nodejs.org/api/esm.html#import-expressions)
```

This approach helps developers understand exactly how to use APIs correctly and reduces confusion about parameter types, optional arguments, and expected behaviors.