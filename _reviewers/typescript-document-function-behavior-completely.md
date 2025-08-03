---
title: Document function behavior completely
description: 'Functions should be documented with comprehensive JSDoc comments that
  cover:

  1. Purpose and behavior description

  2. All parameters with their types and constraints'
repository: microsoft/typescript
label: Documentation
language: TypeScript
comments_count: 7
repository_stars: 105378
---

Functions should be documented with comprehensive JSDoc comments that cover:
1. Purpose and behavior description
2. All parameters with their types and constraints
3. Return value and possible undefined cases
4. Error conditions that may trigger exceptions
5. Deprecation notices when applicable
6. Explanatory comments for complex logic

Example:
```typescript
/**
 * Returns a diagnostic message for ECMAScript module syntax errors
 * in CommonJS files under verbatimModuleSyntax.
 *
 * @param node - The AST node where the error occurred
 * @returns A DiagnosticMessage explaining the error. If the file has a .cts or .cjs extension,
 *          a specific error message for CommonJS files is returned. Otherwise, a more general
 *          error message with suggestions for resolving the issue is returned.
 * @throws {SyntaxError} If the node type is invalid for module syntax checking
 * @deprecated Use getModuleDiagnostic() instead
 */
function getVerbatimModuleSyntaxErrorMessage(node: Node): DiagnosticMessage {
    // Skip validation for non-module files to improve performance
    const sourceFile = getSourceFileOfNode(node);
    const fileName = sourceFile.fileName;
    // ...
}
```