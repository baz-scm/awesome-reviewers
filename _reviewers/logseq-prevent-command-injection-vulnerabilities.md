---
title: Prevent command injection vulnerabilities
description: When implementing shell command execution or CLI features, prioritize
  security by avoiding direct shell execution and implementing robust input validation.
  Simple allow/deny lists for dangerous commands may not provide sufficient protection
  against command injection attacks.
repository: logseq/logseq
label: Security
language: Other
comments_count: 2
repository_stars: 37695
---

When implementing shell command execution or CLI features, prioritize security by avoiding direct shell execution and implementing robust input validation. Simple allow/deny lists for dangerous commands may not provide sufficient protection against command injection attacks.

Consider using established security libraries like shellquote for proper input sanitization, or avoid shell execution entirely when possible. Before exposing command execution capabilities to plugins or user input, thoroughly research and test the security implications.

Example of insufficient protection:
```clojure
(def dangerous-commands
  ["rm" "sudo" "chmod"]) ; This list-based approach may not be comprehensive enough
```

Instead, prefer safer alternatives like:
- Using specific APIs rather than shell commands
- Implementing strict input validation and escaping
- Leveraging security-focused libraries for command sanitization
- Deferring shell execution features until proper security measures are established

The goal is to prevent attackers from injecting malicious commands through user input or plugin interfaces.