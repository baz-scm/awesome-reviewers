---
title: Document Parse Contracts
description: 'Ensure technical documentation describes a strict, consumer-ready contract:
  it must match implemented behavior and clearly tell readers (humans and scripts)
  what they can rely on.'
repository: cline/cline#x
label: Documentation
language: Other
comments_count: 2
repository_stars: 70861
---

Ensure technical documentation describes a strict, consumer-ready contract: it must match implemented behavior and clearly tell readers (humans and scripts) what they can rely on.

Apply this when updating CLI references and machine-readable formats:
- Match reality: behavior and ordering must reflect implementation (e.g., option semantics and result ordering should agree with `--help`/actual output).
- Avoid misleading entries: don’t document options/rows as “accepted” if they’re effectively ignored; remove or explicitly constrain them instead.
- For structured outputs (like JSONL): document invariants (e.g., “one JSON object per line” and required fields) and enumerate only the types/fields that consumers should parse/handle; omit status lines no script needs to act on.
- Keep examples contract-true: include minimal commands showing the non-interactive/required parameters or output shape.

Example (JSONL consumer guidance):
```bash
# Print JSONL, then parse only the event types you handle
cline history --json --limit 10 | jq -r 'select(.type=="run_result" or .type=="agent_event") | .'
```

This prevents documentation from becoming a source of incorrect assumptions for both CLI users and automation scripts.