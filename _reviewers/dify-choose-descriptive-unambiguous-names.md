---
title: Choose descriptive, unambiguous names
description: Select variable, method, and property names that clearly communicate
  their purpose and avoid ambiguity. Prioritize semantic accuracy over brevity, and
  consider the context in which names will be used to prevent confusion.
repository: langgenius/dify
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 114231
---

Select variable, method, and property names that clearly communicate their purpose and avoid ambiguity. Prioritize semantic accuracy over brevity, and consider the context in which names will be used to prevent confusion.

Key principles:
- Use semantically accurate names that reflect the actual purpose (e.g., `affectedNodes` instead of `effectNodes` when referring to nodes that are affected by an operation)
- Avoid naming conflicts by choosing distinct terms when similar concepts coexist (e.g., use `inputs` instead of `variables` when a `variable` property already exists)
- Replace magic strings with enums or constants for better type safety and self-documentation

Example:
```typescript
// Poor: ambiguous and uses magic strings
const effectNodes = findNodes(selector, nodes)
if (permission === 'only_me') { ... }

// Better: clear semantic meaning and structured types
const affectedNodes = findNodes(selector, nodes)
if (permission === DatasetPermission.ONLY_ME) { ... }
```

This approach reduces cognitive load, prevents misunderstandings, and makes code more maintainable by ensuring names accurately represent their underlying concepts.