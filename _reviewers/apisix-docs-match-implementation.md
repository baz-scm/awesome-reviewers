---
title: Docs Match Implementation
description: 'Docs must be verifiable against the actual plugin/runtime behavior:
  schemas (fields/types/requiredness), defaults, and example outputs. Additionally,
  follow the repo’s established doc formatting conventions for things like canonical
  tags and secret-value prefixes.'
repository: apache/apisix
label: Documentation
language: Markdown
comments_count: 16
repository_stars: 16922
---

Docs must be verifiable against the actual plugin/runtime behavior: schemas (fields/types/requiredness), defaults, and example outputs. Additionally, follow the repo’s established doc formatting conventions for things like canonical tags and secret-value prefixes.

Apply this standard as a pre-merge checklist:
- Schema accuracy: ensure every documented config key exists in the plugin schema and has correct type/valid-values.
  - If a field isn’t user-configurable (even if set internally), don’t document it as an input (e.g., don’t advertise `field.type` for `elasticsearch-logger` if only `field.index` is supported).
- Defaults accuracy: if a plugin relies on shared batch-processor defaults, the docs must match the shared default (e.g., don’t claim `max_retry_count=60` when code defaults to `0`).
- Table semantics: keep “Required” as a boolean; move conditional prose into the “Description” column.
- Behavior-faithful examples: example request/response transformations must match real behavior (e.g., regex-based URI rewrites must use patterns that yield exactly what the docs claim, given the runtime replace/match semantics).
- Executable examples: code samples must fully demonstrate the behavior being tested (e.g., streaming handlers must include `data/end/error`, not only metadata).
- Formatting conventions: keep canonical-link markup and other doc wrappers consistent with the rest of the documentation set; use the documented secret prefix conventions (e.g., `$env://...` / `$secret://...`).

Quick example (schema-vs-docs):
```json
// Good: only document fields that the schema actually accepts.
{
  "elasticsearch-logger": {
    "field": {
      "index": "gateway"  // documented + schema-backed
      // DO NOT document "type": "logs" if not accepted by the schema
    }
  }
}
```

Quick example (behavior-faithful rewrite):
- If the runtime only replaces the matched part of the upstream URI, the documented example must use a regex that consumes the segments required to produce the stated final path; otherwise the doc is incorrect.