---
title: Centralize input bounds
description: When validating user-controlled numeric inputs, define allowed min/max
  values in one place and reuse them across both the UI/component props and the validation
  schema. Prevent mismatches where the UI permits one range but the schema enforces
  another (or vice versa), since this breaks input validation guarantees.
repository: infiniflow/ragflow
label: Security
language: TSX
comments_count: 1
repository_stars: 80174
---

When validating user-controlled numeric inputs, define allowed min/max values in one place and reuse them across both the UI/component props and the validation schema. Prevent mismatches where the UI permits one range but the schema enforces another (or vice versa), since this breaks input validation guarantees.

Example:
```ts
const TOP_N_MAX = 200;

export const topnSchema = {
  top_n: z.number().max(TOP_N_MAX).optional(),
};

function TopNFormField({ max = TOP_N_MAX, ...props }: { max?: number }) {
  // Ensure any passed `max` defaults/constraints align with TOP_N_MAX.
  return /* render */ null;
}
```
Practical checklist:
- Use a shared constant (or a single policy source) for allowed bounds.
- Derive component `max`/limits from that constant rather than duplicating numbers.
- Avoid hard-coded schema limits that can diverge from what the component consumer can pass.