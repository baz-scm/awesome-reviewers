---
title: Accurate, Actionable Docs
description: 'When updating technical docs (CLI/API/config/format), make them accurate
  and non-misleading, and write them to help users correctly do the task.


  Apply these rules:'
repository: cline/cline?x=1
label: Documentation
language: Other
comments_count: 3
repository_stars: 70861
---

When updating technical docs (CLI/API/config/format), make them accurate and non-misleading, and write them to help users correctly do the task.

Apply these rules:
1) Don’t document “no-op” features
- If a documented option/behavior “has no effect”, either remove it from the docs or fix the product. Avoid vague “accepted but ignored” language because it invites reliance.

2) Match docs to real behavior
- For each command/flag/config key, state what actually happens (interactive vs non-interactive, defaults, direction of ordering, parameter meaning). Update any doc text that could contradict `--help` or runtime behavior.
- Prefer concrete examples over generic descriptions.

3) For output/format docs, document consumption strategy
- If output is structured/streamed, document the fields a consumer must handle and the safe approach (e.g., scripts should skip message types they don’t use), rather than exhaustively listing every possible line/type.

Example (safe `--json` consumption)
```bash
# Script idea: treat each line as a JSON object and only handle types you care about
cline history --json | while read -r line; do
  type=$(echo "$line" | jq -r .type)
  case "$type" in
    agent_event|run_result) echo "$line" ;;
    *) : ;;  # ignore types you don't parse
  esac
done
```

This standard prevents doc drift, removes dead-feature confusion, and makes docs usable for both humans and automation.