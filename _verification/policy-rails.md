---
title: "Policy rails"
code: "V1058.002"
slug: "policy-rails"
technique: "Output guardrails"
technique_id: "V1058"
technique_slug: "output-guardrails"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Block outputs that leak secrets, change protected files or exceed scope."
repos: 0
craft:
  - "List the protected paths and the actions the bot may not perform."
  - "Scan each output for secret patterns and block the output on a match."
  - "Log every blocked output with the rule it broke, for review."
reverse:
  - "A Colang rails directory for NeMo Guardrails with input and output rail definitions."
  - "A config.yml that lists the input and output rails for the bot."
packages:
  - id: "nemo-guardrails"
    name: "NeMo Guardrails"
    url: "https://github.com/NVIDIA-NeMo/Guardrails"
  - id: "llm-guard"
    name: "LLM Guard"
    url: "https://github.com/protectai/llm-guard"
tools: []
examples: []
---
