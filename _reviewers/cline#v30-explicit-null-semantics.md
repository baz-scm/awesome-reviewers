---
title: Explicit null semantics
description: When handling `null`/`undefined`/empty values, treat them as distinct
  states and make that distinction explicit across schema validation, runtime normalization,
  and persistence/encoding.
repository: cline/cline#v30
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70894
---

When handling `null`/`undefined`/empty values, treat them as distinct states and make that distinction explicit across schema validation, runtime normalization, and persistence/encoding.

**Standard rule**
- Decide the meaning of each input form:
  - **omitted** (`undefined` / missing field)
  - **explicitly null** (`null`)
  - **explicit empty** (`[]`, `""`)
  - **clear vs no-op** for stored records
- Ensure your **TypeScript types, validation schema, runtime normalization, and storage encoding** all implement the same meaning.

**Common failure modes to prevent**
- **Null becomes omit by accident**: e.g., “clear this field” encoded as a value that the decoder treats as omitted, turning a clear into a no-op.
- **Type drift**: signatures say `undefined` but the code normalizes `null` (or vice versa), creating silent behavior gaps.
- **Merge/replace confusion**: omitted fields decode into empty arrays (e.g., protobuf), causing “keep previous” logic to be skipped unintentionally.
- **Wrong-branch fallback**: missing/mismatched auth/config facts should not silently route into a default behavior that changes semantics.

**How to apply**
1. **Normalize only where you intend**. If `null` should behave like omission for a specific operation, normalize at runtime and document it.
2. **Preserve “clear” semantics in persistence**. If the system needs a true clear, encode it in the persistence layer in a way that cannot be mistaken for omission.
3. **Use meaningful-override checks** when merging updates/retries:
   - override only when the incoming value is present *and* meaningful (not just “it exists but decodes to empty due to omission”).

**Illustrative pattern**
```ts
// Decide: omitted => keep existing, explicit null => clear, empty array => set empty.
function applyUpdate<T>(existing: T, incoming: { value?: T | null }): T {
  if (incoming.value === undefined) return existing; // omitted
  if (incoming.value === null) return /* cleared */ (undefined as unknown as T);
  return incoming.value; // includes empty arrays/strings if T supports them
}

// Storage encoding should distinguish clear vs omit ({} vs null), matching decoder behavior.
```

**Testing requirement**
- Add unit tests that cover all three cases: omitted, explicit `null`, and explicit empty—especially for update/merge and persistence clear-vs-no-op paths.