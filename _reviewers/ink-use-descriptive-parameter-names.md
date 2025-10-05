---
title: Use descriptive parameter names
description: Choose parameter names that clearly communicate their purpose and avoid
  confusion with similar concepts. Avoid generic or ambiguous names that could be
  misinterpreted.
repository: vadimdemedes/ink
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 31825
---

Choose parameter names that clearly communicate their purpose and avoid confusion with similar concepts. Avoid generic or ambiguous names that could be misinterpreted.

When naming parameters, consider:
- What the parameter actually represents, not just its technical type
- Whether the name could be confused with other common programming concepts
- If the parameter type changes, update the name to match

Example of unclear naming:
```typescript
export function useInput(
	inputHandler: (input: string, meta: Meta) => void
```

Better alternatives:
```typescript
export function useInput(
	inputHandler: (input: string, metadata: InputMetadata) => void
	// or
	inputHandler: (input: string, key: KeyInfo) => void
```

The name `meta` is ambiguous because it could be confused with "meta keys" (a different keyboard concept), while `metadata` or `key` clearly indicate what the parameter contains.