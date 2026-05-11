---
title: Explicit Error Narrowing
description: 'When using data/mutation libraries, treat error handling as a two-step
  process: (1) type errors conservatively at the boundary, and (2) implement recovery/UI
  logic that matches the library’s actual error-state semantics.'
repository: tanstack/query
label: Error Handling
language: Markdown
comments_count: 5
repository_stars: 49380
---

When using data/mutation libraries, treat error handling as a two-step process: (1) type errors conservatively at the boundary, and (2) implement recovery/UI logic that matches the library’s actual error-state semantics.

**1) Use conservative global error typing**
- Prefer a global error type of `unknown` (or keep the default) so call sites must explicitly narrow before reading properties.

**2) Don’t assume placeholder/optimistic flows preserve error status**
- If you migrate from `keepPreviousData` to `placeholderData`, update UI logic: `placeholderData` puts the query into `success` state, even though background refetches could fail.

**3) Wire recovery callbacks to the correct inputs**
- For optimistic rollback, use the value returned from `onMutate` (as provided to `onError`) rather than relying on older callback signatures.

**4) Place try/catch only where the promise can throw**
- Some helper calls (e.g., prefetch) return a `Promise<void>` that you can await but “will never throw”, so don’t wrap them in try/catch as if they were failing operations.

Example (TanStack Query placeholder + conservative error typing):

```ts
import { useQuery } from '@tanstack/react-query'

useQuery({
  queryKey: ['some-query'],
  queryFn: async () => {
    // ensure you narrow before using error details
    if (Math.random() > 0.5) throw new Error('some error')
    return 42
  },
  // placeholderData replaces keepPreviousData
  placeholderData: (previous) => previous,
})

// At call sites with global error = unknown, narrow explicitly before using properties.
// Example:
// if (error instanceof SomeError) { error.code ... }
```

Follow these rules to prevent accidental “error access” without narrowing, avoid UI bugs caused by changed status semantics, and ensure rollback and error handling occur in the right place.