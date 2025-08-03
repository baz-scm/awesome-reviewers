---
title: Names reveal semantic purpose
description: Choose names that clearly communicate the semantic purpose and behavior
  of code elements. Variable and function names should precisely reflect their role,
  return type, and intended usage.
repository: microsoft/typescript
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 105378
---

Choose names that clearly communicate the semantic purpose and behavior of code elements. Variable and function names should precisely reflect their role, return type, and intended usage.

Key guidelines:
1. Function names should indicate their behavior and return type
2. Use distinct names for related but different concepts
3. Choose specific over generic names
4. Fix misleading names immediately

Example:
```typescript
// Poor naming
function isGlobalType(checker: TypeChecker, symbol: Symbol) {
    return checker.resolveName(symbol.name, undefined, SymbolFlags.Type, false);
}

// Better naming - reflects actual behavior
function canResolveTypeGlobally(checker: TypeChecker, typeName: string) {
    return checker.resolveName(typeName, undefined, SymbolFlags.Type, false);
}

// Poor naming - reusing variable
let initializer = getCandidateVariableDeclarationInitializer(declaration);
if (initializer) { ... }
initializer = getDestructuredInitializer(declaration);

// Better naming - distinct purposes
let directInit = getCandidateVariableDeclarationInitializer(declaration);
if (directInit) { ... }
let destructuredInit = getDestructuredInitializer(declaration);
```