---
title: "Logic and correctness review"
id: "V1035"
slug: "logic-and-correctness-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Reads the change for wrong behaviour: off-by-one, inverted conditions, missed error paths, broken invariants, race conditions."
subtechniques:
  - id: "V1035.001"
    name: "Logic bug review"
    description: "Look for conditions, loops and state transitions that do not match intent."
  - id: "V1035.002"
    name: "Error path review"
    description: "Check failures, retries and partial writes."
  - id: "V1035.003"
    name: "Type and contract consistency"
    description: "Check that values crossing module boundaries keep their meaning."
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
craft:
  - "Give the reviewer the intent, the diff and retrieved context."
  - "Ask for findings only with a concrete triggering input or state."
  - "Validate each finding before posting (see Finding validation)."
reverse:
  - "Review bot workflows (claude-code-action, pr-agent) and their prompt files."
---
