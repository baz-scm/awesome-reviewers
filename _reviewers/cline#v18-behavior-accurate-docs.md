---
title: Behavior-Accurate Docs
description: Documentation must be precise, implementation-aligned, and actionable—especially
  for user-facing paths, CLI flag semantics, and machine-readable output.
repository: cline/cline#v18
label: Documentation
language: Other
comments_count: 3
repository_stars: 70884
---

Documentation must be precise, implementation-aligned, and actionable—especially for user-facing paths, CLI flag semantics, and machine-readable output.

Apply these rules:
1. **Platform-correct paths**: If you document filesystem locations using `~` or other conventions, verify and clarify how they resolve on major platforms (e.g., Windows). Prefer explicit examples for common OSes when ambiguity would confuse users.
   - Example rule: “Show both Unix and Windows paths if users exist on both, or explicitly state what `~` resolves to on Windows.”

2. **No misleading options/semantics**: Ensure every documented option, default, ordering, and restriction matches the actual behavior (`--help`, logs, release notes). Avoid documenting options as “accepted but ignored” unless the CLI truly does that—and if you do, explain the rationale and current status clearly.

3. **Consumer-first output docs** (JSON/streams): For structured output, document the exact schema/types that matter and instruct how to handle unknown/unneeded types (e.g., “skip lines where `type` is not relevant”). Keep examples representative of current behavior.

Code/doc example (structured output parsing):
```bash
# If using --json, treat it as a stream of JSON objects per line.
# Parse only the types your script needs; ignore others.
cline history --json | jq -c 'select(.type=="run_result" or .type=="agent_event")'
```

Outcome: fewer surprises during usage and safer automation because docs match the real CLI output and reflect platform realities.