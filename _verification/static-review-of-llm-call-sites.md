---
title: "Static review of LLM call sites"
code: "V1039.001"
slug: "static-review-of-llm-call-sites"
technique: "LLM application security review"
technique_id: "V1039"
technique_slug: "llm-application-security-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Check how untrusted text reaches prompts and how outputs reach tools or HTML."
repos: 0
craft:
  - "List every call site that builds a prompt from outside input."
  - "Mark each place where untrusted text enters a prompt and each place where generated output reaches a tool, a shell or HTML."
  - "Review each marked site on every change that touches it."
reverse:
  - "Prompt template files or prompt-building functions with a named owner."
  - "Code paths where generated output reaches an exec, shell or innerHTML call with a sanitizer step between them."
  - "A pull request template item that asks about new prompt inputs."
packages: []
tools: []
examples: []
---
