---
title: Explicit Undefined Handling
description: When a value is intentionally absent (e.g., an optional callback prop
  or required classification fields), represent that absence explicitly and don’t
  let missing/nullable data silently pass as “valid”.
repository: diegosouzapw/OmniRoute
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 33162
---

When a value is intentionally absent (e.g., an optional callback prop or required classification fields), represent that absence explicitly and don’t let missing/nullable data silently pass as “valid”.

**Rules of thumb**
1. **Optional callbacks:** If there’s no behavior to run, prefer passing `undefined` (or omitting the prop) over a noop lambda—unless the component specifically requires a non-null function.
2. **Strict filtering:** When narrowing collections based on optional fields, require the expected properties. Don’t write predicates that treat missing fields as matching (e.g., `!m.type || ...`). This prevents unrelated items (with absent fields) from being included.

**Examples**
```tsx
// 1) Optional callback: use undefined instead of noop
<Toggle
  size="xs"
  checked={!allDisabled}
  onChange={undefined} // or simply omit onChange
/>

// 2) Strict null/undefined-aware filtering
const sttModels = models.filter(
  (m) => m.type === "audio" && m.subtype === "transcription"
);
// Avoid: (m) => !m.type || (m.type === "audio" && ...)
```

This approach reduces accidental behavior (no-op handlers) and avoids UI/data contamination caused by missing optional fields being treated as matches.