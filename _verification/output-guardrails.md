---
title: "Output guardrails"
id: "V1058"
slug: "output-guardrails"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Validates what an automated reviewer or fixer produces before it is posted or committed: schema, policy and safety checks."
subtechniques:
  - id: "V1058.001"
    name: "Schema validation"
    description: "Reject malformed structured output and retry."
  - id: "V1058.002"
    name: "Policy rails"
    description: "Block outputs that leak secrets, change protected files or exceed scope."
packages:
  - id: "guardrails"
    name: "Guardrails AI"
    url: "https://github.com/guardrails-ai/guardrails"
  - id: "nemo-guardrails"
    name: "NeMo Guardrails"
    url: "https://github.com/NVIDIA-NeMo/Guardrails"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
craft:
  - "Define the output schema and validate every response."
  - "List protected paths and actions the bot may not take."
  - "Log every blocked output for review."
reverse:
  - "Guardrail config files or validators around model calls."
---
