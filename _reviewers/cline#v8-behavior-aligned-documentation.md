---
title: Behavior-aligned documentation
description: 'Documentation should reflect what the product actually does and what
  the target reader needs to act on.


  Apply these rules:

  - Don’t document no-ops: if an option/field “has no effect,” remove it from docs,
  or only include it with an explicit caveat that it’s ignored and why.'
repository: cline/cline#v8
label: Documentation
language: Other
comments_count: 5
repository_stars: 70867
---

Documentation should reflect what the product actually does and what the target reader needs to act on.

Apply these rules:
- Don’t document no-ops: if an option/field “has no effect,” remove it from docs, or only include it with an explicit caveat that it’s ignored and why.
- Keep examples behavior-accurate: ensure CLI/workflow examples match real argument parsing and routing (e.g., if the command forwards args after a position, put options before that position when they must be parsed by the CLI).
- Scope structured output docs to consumers: for JSONL/streamed logs, document the fields and meaning of types that scripts/agents should parse; explicitly instruct readers to skip types they don’t use rather than claiming completeness.
- Be explicit across platforms: avoid relying on ambiguous shorthand for paths (like `~`) when it can map differently on Windows. Either document the Windows equivalent (or the exact environment behavior) or phrase guidance in a way that doesn’t assume POSIX semantics.

Example (JSONL):
```md
With `--json`, output is JSON Lines. Every line includes `type` and `ts`.
Scripts should parse only the types they need; ignore other `type` values.
```