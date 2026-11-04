---
title: "LLM application security review"
id: "V1039"
slug: "llm-application-security-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Reviews code that calls models for the OWASP Top 10 for LLM applications: prompt injection, output handling, excessive agency, unbounded consumption."
subtechniques:
  - id: "V1039.001"
    name: "Static review of LLM call sites"
    description: "Check how untrusted text reaches prompts and how outputs reach tools or HTML."
  - id: "V1039.002"
    name: "Red-team probing"
    description: "Send adversarial prompts to a running application and score the responses."
  - id: "V1039.003"
    name: "Runtime input and output scanning"
    description: "Scan prompts and responses in production for injection and leakage."
packages:
  - id: "garak"
    name: "garak"
    url: "https://github.com/NVIDIA/garak"
  - id: "promptfoo"
    name: "promptfoo"
    url: "https://github.com/promptfoo/promptfoo"
  - id: "llm-guard"
    name: "LLM Guard"
    url: "https://github.com/protectai/llm-guard"
craft:
  - "List every place untrusted text enters a prompt and every place model output is executed or rendered."
  - "Run a red-team suite against those paths in CI."
  - "Cap tokens, tool calls and spend per request."
reverse:
  - "promptfoo or garak config, prompt templates, and tool definitions in the repository."
---
