---
title: Nil-safe assignment
description: 'When fields/items are optional, treat `nil`/empty as a first-class state:
  guard against nil dereferences, sanitize outputs, and never overwrite meaningful
  non-nil data with `nil`.'
repository: looplj/axonhub
label: Null Handling
language: Go
comments_count: 4
repository_stars: 4808
---

When fields/items are optional, treat `nil`/empty as a first-class state: guard against nil dereferences, sanitize outputs, and never overwrite meaningful non-nil data with `nil`.

Apply:
- **Nil-aware assignment**: only assign optional pointers/values when they are non-nil (avoid forcing `XContent = nil`).
- **Defensive branching**: when logic depends on “completion”, don’t assume related payload fields are non-empty; keep/introduce fallbacks for `len(...)==0`.
- **Output sanitization**: filter `nil`/empty stream elements so downstream consumers see only valid items.
- **Normalize optional inputs**: if a downstream expects a non-pointer, convert/normalize with explicit nil checks rather than unsafe deref.

Example:
```go
// Nil-aware mapping: don’t overwrite with nil
if len(m.ReasoningDetails) > 0 {
    // ... build from details ...
} else if m.Reasoning != nil {
    m.ReasoningContent = m.Reasoning
}

// Defensive fallback for empty payload
if len(responseBody) > 0 {
    persistAggregatedResponse(ctx, responseBody, meta)
} else {
    // aggregated “completed” doesn’t guarantee responseBody presence
    persistResponseChunks(ctx)
}

// Stream sanitization: filter nil items
for _, item := range items {
    if item == nil {
        continue
    }
    emit(item)
}
```