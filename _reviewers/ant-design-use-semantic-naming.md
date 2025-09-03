---
title: Use semantic naming
description: Choose semantic, non-redundant names that clearly express intent and
  context. Remove unnecessary prefixes when the context is already clear, use semantic
  design tokens instead of hardcoded values, and prefer precise type definitions over
  generic ones.
repository: ant-design/ant-design
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 95882
---

Choose semantic, non-redundant names that clearly express intent and context. Remove unnecessary prefixes when the context is already clear, use semantic design tokens instead of hardcoded values, and prefer precise type definitions over generic ones.

Key practices:
- Remove redundant prefixes: Use `quickJumperInputWidth` instead of `paginationQuickJumperInputWidth` when the context (pagination) is already established
- Use semantic design tokens: Replace hardcoded values like `8px` with semantic tokens like `token.marginXS` 
- Avoid unnecessary type aliases: Export functions directly rather than maintaining separate type definitions when the function signature is self-explanatory
- Use precise union types: Specify exact values like `'timePicker' | 'datePicker'` instead of generic `string` types

Example:
```typescript
// ❌ Redundant prefix and hardcoded value
const paginationQuickJumperInputWidth = '8px';

// ✅ Semantic naming
const quickJumperInputWidth = token.marginXS;

// ❌ Unnecessary type alias
type UseOrientation = (orientation?: Orientation) => [Orientation, boolean];
const useOrientation: UseOrientation = (orientation) => { ... };

// ✅ Direct export with clear signature
export default function useOrientation(orientation?: Orientation): [Orientation, boolean] { ... }
```