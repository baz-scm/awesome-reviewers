---
title: Document Parse-Relevant Behavior
description: Technical docs for CLI/JSON outputs should be behavior-accurate and scoped
  to what developers (and scripts) can safely rely on. Avoid implying that an option/type
  is supported when it’s not; keep tables/examples consistent with real outputs and
  ordering semantics. For machine-readable formats (e.g., `--json`), document the
  exact per-line schema and...
repository: cline/cline#v10
label: Documentation
language: Other
comments_count: 2
repository_stars: 70869
---

Technical docs for CLI/JSON outputs should be behavior-accurate and scoped to what developers (and scripts) can safely rely on. Avoid implying that an option/type is supported when it’s not; keep tables/examples consistent with real outputs and ordering semantics. For machine-readable formats (e.g., `--json`), document the exact per-line schema and explicitly tell consumers which message types/fields they must parse vs which types can be skipped.

Apply this checklist:
- Verify docs against the actual CLI/API behavior (including defaults, sort order, and whether interactions are prompted).
- Don’t describe unsupported options as “accepted but ignored”; either implement them or omit/remove the docs.
- Keep examples and tables consistent with the output (timestamps, field types, and per-line structure).
- For JSON/streaming logs: list only the types/fields that parsing logic should act on; instruct scripts to ignore other/unneeded types.

Example (script pattern for `--json` output):
```bash
# Expect one JSON object per line; parse only the types you need.
cline history --json | while IFS= read -r line; do
  type=$(echo "$line" | jq -r '.type')
  case "$type" in
    run_result|agent_event|hook_event) echo "$line" ;; # handle only relevant types
    *) : ;; # skip everything else
  esac
done
```