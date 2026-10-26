---
title: Doc as Parsing Contract
description: 'Treat docs for CLI/SDK outputs as a strict, parseable contract.


  - Match reality: ensure every documented option, default, ordering, and behavior
  is consistent with `--help`/implementation. If an option is omitted/unsupported
  or would be “accepted but ignored,” remove it from the contract tables rather than
  implying it can be relied on.'
repository: Cline/Cline
label: Documentation
language: Other
comments_count: 2
repository_stars: 70840
---

Treat docs for CLI/SDK outputs as a strict, parseable contract.

- Match reality: ensure every documented option, default, ordering, and behavior is consistent with `--help`/implementation. If an option is omitted/unsupported or would be “accepted but ignored,” remove it from the contract tables rather than implying it can be relied on.
- Scope to what consumers act on: for JSON/streaming outputs, document the required envelope/fields and the event types that parsers should process. Explicitly instruct consumers to skip/ignore types they don’t use.
- Prefer correctness over completeness: don’t list non-actionable/status-only lines in the “parseable types” table.

Example (JSON parsing guidance in docs):
```text
With --json, the CLI prints one JSON object per line. Every line includes:
- type
- ts (ISO 8601)

Scripts should switch on type, handle only event types they need, and ignore the rest.
```