---
title: "Error path review"
code: "V1035.002"
slug: "error-path-review"
technique: "Logic and correctness review"
technique_id: "V1035"
technique_slug: "logic-and-correctness-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Check failures, retries and partial writes."
repos: 0
craft:
  - "Ask the reviewer to list each call that can fail and what the change does on failure."
  - "Check retries, partial writes and cleanup code in the diff."
  - "Post a finding only when a failure leaves state inconsistent."
reverse:
  - "Review bot configuration that includes an error-handling checklist."
  - "Review comments that describe a failed write or a missing rollback."
  - "Test cases named for failure, timeout or retry paths in the changed module."
packages:
  - id: "pr-agent"
    name: "PR-Agent"
    url: "https://github.com/The-PR-Agent/pr-agent"
  - id: "claude-code-action"
    name: "Claude Code Action"
    url: "https://github.com/anthropics/claude-code-action"
  - id: "openhands"
    name: "OpenHands"
    url: "https://github.com/OpenHands/OpenHands"
tools: []
examples: []
---
