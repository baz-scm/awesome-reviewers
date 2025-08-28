---
title: API header management
description: Establish consistent patterns for handling headers in API clients to
  avoid duplication and ensure predictable behavior. When designing API client interfaces,
  clearly define header precedence rules and avoid setting headers in multiple locations
  unless absolutely necessary.
repository: kilo-org/kilocode
label: API
language: TypeScript
comments_count: 3
repository_stars: 7302
---

Establish consistent patterns for handling headers in API clients to avoid duplication and ensure predictable behavior. When designing API client interfaces, clearly define header precedence rules and avoid setting headers in multiple locations unless absolutely necessary.

**Key principles:**
1. **Header Precedence**: Decide whether persistent headers should override request-specific headers or vice versa. Document this decision clearly. As one developer noted: "if the provider made the effort to set a persistent header, that it shouldn't be overridden."

2. **Avoid Duplication**: Don't set the same headers in multiple places unless there's a technical requirement. If duplication is necessary, document why both locations are needed.

3. **Clean Construction**: Use efficient header object construction patterns instead of multiple mutations.

**Example of clean header construction:**
```typescript
// Preferred: Clean, efficient construction
const headers = {
  'anthropic-beta': betas.length > 0 ? betas.join(",") : undefined,
  'idempotency-key': taskId && checkpointNumber !== undefined ? this.getIdempotencyKey(taskId, checkpointNumber) : undefined,
}

// Avoid: Multiple object mutations
const headers: Record<string, string> = {}
if (betas.length > 0) {
  headers["anthropic-beta"] = betas.join(",")
}
if (taskId && checkpointNumber !== undefined) {
  headers["idempotency-key"] = this.getIdempotencyKey(taskId, checkpointNumber)
}
```

This ensures API clients are maintainable, predictable, and efficient in their header management.