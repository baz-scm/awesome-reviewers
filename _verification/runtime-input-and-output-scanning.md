---
title: "Runtime input and output scanning"
code: "V1039.003"
slug: "runtime-input-and-output-scanning"
technique: "LLM application security review"
technique_id: "V1039"
technique_slug: "llm-application-security-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Scan prompts and responses in production for injection and leakage."
repos: 0
craft:
  - "Place a scanner in front of the prompt path and behind the response path."
  - "Block or redact the content the scanner flags, and log the flag without the content."
  - "Track the rate of flagged inputs and outputs per route."
reverse:
  - "Scanner calls that wrap the request and response functions in the service."
  - "A guardrails or rails config directory in the repository."
  - "Logs or metrics that count scanner flags per route."
packages:
  - id: "llm-guard"
    name: "LLM Guard"
    url: "https://github.com/protectai/llm-guard"
  - id: "guardrails"
    name: "Guardrails AI"
    url: "https://github.com/guardrails-ai/guardrails"
  - id: "nemo-guardrails"
    name: "NeMo Guardrails"
    url: "https://github.com/NVIDIA-NeMo/Guardrails"
tools: []
examples: []
---
