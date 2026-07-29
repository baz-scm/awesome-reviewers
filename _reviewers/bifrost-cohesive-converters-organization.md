---
title: Cohesive Converters Organization
description: 'Keep Go files cohesive by responsibility, and make branching/conversion
  logic easy to extend.


  **1) Put types where they belong**

  - Move request/response structs (and their `GetExtraParams` helpers) into `types.go`.'
repository: maximhq/bifrost
label: Code Style
language: Go
comments_count: 11
repository_stars: 6862
---

Keep Go files cohesive by responsibility, and make branching/conversion logic easy to extend.

**1) Put types where they belong**
- Move request/response structs (and their `GetExtraParams` helpers) into `types.go`.
- Keep provider-specific files (e.g., `embedding.go`) for converter/transform functions only.

**2) Keep conversion logic readable**
- Prefer `guard + switch` over repeated inline `if x.Type == ...` checks.
- Use small, named helpers for steps like “convert content parts”, “apply extra params”, “encode/decode media”.

Example pattern:
```go
if chunk.Index == nil || chunk.ContentBlock == nil {
  return nil, nil, false
}

switch chunk.ContentBlock.Type {
case AnthropicContentBlockTypeToolUse:
  // structured handling
case AnthropicContentBlockTypeRedactedThinking:
  // structured handling
default:
  return nil, nil, false
}
```

**3) DRY repeated utilities safely**
- Extract near-verbatim duplication into shared helpers (e.g., reserving terminal chunk indexes), but keep fields separate when dedup semantics differ.

**4) Centralize “magic” values**
- Move status/reason strings and other repeated constants into `schemas` (or a shared constants module) and reuse them across paths.

**5) Prefer strong typing / reuse helpers**
- Avoid `map[string]any` when the project has a structured type (e.g., `schemas.OrderedMap`).
- Use generics where it meaningfully removes duplicated helper functions (e.g., pointer equality for multiple primitives).

This reduces churn when adding new providers/types, makes reviews faster, and prevents subtle behavior drift from copy/pasted logic.