---
title: Behavioral Documentation Contracts
description: 'When writing documentation (especially CLI/API docs), treat it as an
  executable contract: describe the exact triggers/semantics, include non-obvious
  caveats, and ensure examples/tables match runtime behavior.'
repository: cline/cline#v2
label: Documentation
language: Other
comments_count: 3
repository_stars: 70861
---

When writing documentation (especially CLI/API docs), treat it as an executable contract: describe the exact triggers/semantics, include non-obvious caveats, and ensure examples/tables match runtime behavior.

Apply these rules:
- **Document caveats as classes, not lists:** If behavior depends on provider/tooling, explain the underlying condition (e.g., “providers that run tool processing themselves”) rather than an incomplete name list.
- **Keep docs truthful:** Do not describe options as “accepted but ignored.” If something is omitted, explain why (so readers won’t assume they missed an advertised feature).
- **Specify machine-readable formats precisely:** For structured output (e.g., `--json`), document fields/types, the one-record-per-line rule, and how consumers should handle multiple record types (e.g., “skip types you don’t use”).

Example (JSON consumer guidance):
```pseudo
for each line in cli_output:
  obj = parse_json(line)
  if obj.type not in {"run_result","hook_event"}:
    continue   // explicitly skip unneeded types
  handle(obj)
```