---
title: Docs Truthfulness
description: Ensure technical documentation stays accurate and automation-ready. If
  behavior is broken or unsupported, prefer removing the doc entry (or clearly marking
  it as non-functional with a concrete caveat and next steps) rather than implying
  the option is usable. When exceptions exist (e.g., features not firing for certain
  provider classes), explain the caveat...
repository: cline/cline#v6
label: Documentation
language: Other
comments_count: 3
repository_stars: 70864
---

Ensure technical documentation stays accurate and automation-ready. If behavior is broken or unsupported, prefer removing the doc entry (or clearly marking it as non-functional with a concrete caveat and next steps) rather than implying the option is usable. When exceptions exist (e.g., features not firing for certain provider classes), explain the caveat in user-centric terms and define the scope of the exception. For CLI/SDK automation surfaces, specify the exact wire format (e.g., one JSON object per line), field meanings/types, and parsing rules—including what consumers should ignore.

Example (automation-friendly output guidance):
```text
With --json, output is newline-delimited JSON.
Each line is a JSON object with:
- type: one of {"agent_event","hook_event","run_result","run_aborted"}
- ts: ISO 8601 timestamp (string)

Scripts should parse only the types they act on, and ignore the rest.
```