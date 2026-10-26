---
title: Keep Docs Truthful
description: 'All documentation must match the product’s actual behavior and be written
  for the document’s audience (humans vs scripts).


  Apply this standard:

  - Deprecations/removed features: if a feature no longer works, remove stale guidance
  or rewrite it to state the real behavior. Don’t imply it’s effective (especially
  for security/access control).'
repository: cline/cline#v12
label: Documentation
language: Other
comments_count: 3
repository_stars: 70872
---

All documentation must match the product’s actual behavior and be written for the document’s audience (humans vs scripts).

Apply this standard:
- Deprecations/removed features: if a feature no longer works, remove stale guidance or rewrite it to state the real behavior. Don’t imply it’s effective (especially for security/access control).
- Avoid “accepted but ignored” messaging: if an option/behavior is not meaningful, don’t document it in a way that suggests readers should use it.
- Stay consistent with `--help` and implementation: verify examples, option semantics, defaults, and ordering (e.g., what `--limit` returns) against the current CLI.
- For machine-readable output (e.g., `--json`): document the current object/line structure and the set of message/event categories a consumer might see; explicitly instruct consumers to skip types they don’t handle.

Example (safe `--json` guidance for scripts):
```bash
cline run ... --json | while read -r line; do
  # Each line is a JSON object with at least: type + ts (and type-specific fields)
  # If the type isn't one this script handles, skip it.
  case "$(echo "$line" | jq -r .type)" in
    agent_event|run_result) echo "$line" ;;
    *) ;; # skip other types
  esac
done
```