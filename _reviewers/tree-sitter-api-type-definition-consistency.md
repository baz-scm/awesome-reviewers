---
title: API type definition consistency
description: When modifying API type definitions, ensure all related definition files
  are updated consistently and dependencies are properly managed. API types often
  exist in multiple formats (TypeScript definitions, JSON schemas, etc.) and must
  be kept in sync to maintain a coherent client interface.
repository: tree-sitter/tree-sitter
label: API
language: TypeScript
comments_count: 2
repository_stars: 21799
---

When modifying API type definitions, ensure all related definition files are updated consistently and dependencies are properly managed. API types often exist in multiple formats (TypeScript definitions, JSON schemas, etc.) and must be kept in sync to maintain a coherent client interface.

Key practices:
- Update all corresponding definition files when adding or modifying API types
- Verify that type dependencies are declared in the correct package.json section (dependencies/peerDependencies vs devDependencies)
- Use appropriate type modifiers (e.g., `Partial<T>` for optional parameters rather than requiring all properties)
- Maintain consistency between auto-generated and manually edited definition files

Example from the discussions:
```typescript
// When adding a new rule type
type ReservedRule = { type: 'RESERVED'; content: Rule; context_name: string };
// Also update grammar.schema.json with corresponding schema definition

// Use proper type modifiers for optional parameters
export default function MainModuleFactory(options?: Partial<EmscriptenModule>): Promise<MainModule>;
// Rather than requiring all EmscriptenModule properties
```

This ensures that API consumers have accurate, complete type information and that the API surface remains consistent across all definition formats.