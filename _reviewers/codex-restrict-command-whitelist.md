---
title: Restrict command whitelist
description: When configuring command whitelists for auto-approval, include only commands
  with limited capabilities that cannot be exploited for malicious purposes. Powerful
  tools like text editors (e.g., vim) should be avoided as they provide broad system
  access and functionality that could introduce security vulnerabilities if auto-approved.
repository: openai/codex
label: Security
language: Markdown
comments_count: 1
repository_stars: 31275
---

When configuring command whitelists for auto-approval, include only commands with limited capabilities that cannot be exploited for malicious purposes. Powerful tools like text editors (e.g., vim) should be avoided as they provide broad system access and functionality that could introduce security vulnerabilities if auto-approved.

Instead, prefer commands with specific, limited functionality such as `nl` (number lines). Evaluate each command for its potential security impact before adding it to the whitelist.

Example:
```
# Recommended
commandWhitelist:
  - "nl"
  - "cat"
  - "grep"

# Not recommended
commandWhitelist:
  - "vim"  # Avoid - provides too much functionality and system access
  - "bash" # Avoid - allows arbitrary command execution
```

Always ask: "What's the worst that could happen if this command is automatically approved and executed?" If the answer involves potential system compromise or data exposure, don't whitelist it.