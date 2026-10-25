---
title: Stable API Evolution Rules
description: 'When evolving any API surface that produces structured, machine-readable
  data (JSON event streams, protobuf messages), design for safe evolution:


  1) Document a stable parse contract'
repository: cline/CLINE
label: API
language: Other
comments_count: 2
repository_stars: 70839
---

When evolving any API surface that produces structured, machine-readable data (JSON event streams, protobuf messages), design for safe evolution:

1) Document a stable parse contract
- For line-delimited JSON/event streams, define the required envelope fields (e.g., `type` and `ts`) and how each `type` maps to its payload.
- Explicitly instruct clients to **skip/ignore types they don’t use** (so adding new event types doesn’t break existing scripts).

2) Preserve compatibility when changing schemas
- For protobuf enums, never reuse removed numeric tags or names. If an enum value is removed, mark it as reserved:
```proto
enum ClineAsk {
  // ... existing values ...
  // Removed value: REPORT_BUG = 14;
  reserved 14;
  reserved "REPORT_BUG";
}
```

3) Keep docs aligned with actual output/semantics
- Ensure the API reference reflects the real set of event types and parsing guidance, and that tables/listings represent what clients should parse (not every internal/status line).

Apply this standard anytime you change:
- Streaming or event-based JSON formats (including `--json`/SSE-like outputs)
- Protobuf enums used across versions
- Any documentation that defines how clients should interpret or filter machine-readable outputs