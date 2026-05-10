---
title: Sanitize untrusted tags
description: Treat any tag/markup coming from user input, LLM output, or external
  commands as untrusted. Validate and sanitize it at the earliest boundary before
  embedding into JSON or rendering in the UI—e.g., strip/escape disallowed tags so
  they can’t break parsers or visuals.
repository: agent0ai/agent-zero
label: Security
language: Shell
comments_count: 1
repository_stars: 17612
---

Treat any tag/markup coming from user input, LLM output, or external commands as untrusted. Validate and sanitize it at the earliest boundary before embedding into JSON or rendering in the UI—e.g., strip/escape disallowed tags so they can’t break parsers or visuals.

Example (shell boundary sanitization):
```sh
# sanitize_tags.sh
# Remove/neutralize disallowed tags before downstream UI/JSON handling
sanitize_tags() {
  # Example: drop <thinking>...</thinking>
  sed -E 's#<\/?thinking[^>]*>##g'
}

INPUT="$1"
SAFE_INPUT="$(printf '%s' "$INPUT" | sanitize_tags)"
# Use $SAFE_INPUT for any JSON generation or UI rendering
```

Apply this by: (1) defining allowed vs. disallowed tags, (2) sanitizing/escaping before JSON construction and before UI templating/rendering, and (3) adding automated tests for payloads that previously broke visuals/JSON (e.g., special tags).