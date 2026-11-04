---
title: "Logic bug review"
code: "V1035.001"
slug: "logic-bug-review"
technique: "Logic and correctness review"
technique_id: "V1035"
technique_slug: "logic-and-correctness-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Look for conditions, loops and state transitions that do not match intent."
repos: 0
craft:
  - "Give the reviewer the change, its linked intent and the surrounding code."
  - "Ask for a finding only with a concrete input or state that triggers the bug."
  - "Post a finding only after a second check confirms the triggering input."
reverse:
  - "A review workflow that runs pr-agent or claude-code-action on pull requests."
  - "Prompt or instruction files for the review bot in the repository."
  - "Review comments that name a specific input and the line it breaks."
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
