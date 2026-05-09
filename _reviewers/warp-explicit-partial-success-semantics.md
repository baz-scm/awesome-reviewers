---
title: Explicit Partial-Success Semantics
description: When an API operation can be “partially successful” (or yields an empty
  but non-error outcome), encode that distinction explicitly in the response/protocol
  so callers can take correct next actions.
repository: warpdotdev/warp
label: API
language: Markdown
comments_count: 3
repository_stars: 56893
---

When an API operation can be “partially successful” (or yields an empty but non-error outcome), encode that distinction explicitly in the response/protocol so callers can take correct next actions.

Apply this standard:
- Never use a plain `Success` with an empty result to represent distinct conditions like “requested line range is beyond EOF”.
- If the system must return per-item results while still reporting per-item problems, extend the *Success* shape with a dedicated field (e.g., `missing_ranges: [...]` / `failed_ranges: [...]`) instead of forcing an all-or-nothing `Failure` or misusing an existing field with different semantics (e.g., treating “range missing” as “file missing”).
- Keep server/protocol status modeling explicit and stateful: expose machine-readable `state` enums and failure categories; prefer bulk initialization/status RPCs over repeated per-entity polling when clients need initial state.

Example pattern (server response shape):
```rust
// Instead of: ReadFilesResult::Success { files: vec![] }
// Use something like:
ReadFilesResult::Success {
  files: vec![/* successfully read files */],
  missing_ranges: vec![
    MissingRange { path: "a.txt", line_range: (1891, 2090) }
  ],
}

// Or, if per-file success is granular:
ReadFilesResult::Success {
  per_file: vec![
    PerFileResult::Ok { path: "a.txt", segments: vec![...] },
    PerFileResult::MissingRange { path: "b.txt", requested: (1891, 2090), eof: 1237 },
  ]
}
```

This keeps the API truthful, prevents misleading UI states, and lets agent/client logic “course-correct” without breaking the ability to return other successfully retrieved items.