---
title: "Schema validation"
code: "V1058.001"
slug: "schema-validation"
technique: "Output guardrails"
technique_id: "V1058"
technique_slug: "output-guardrails"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Reject malformed structured output and retry."
repos: 0
craft:
  - "Define the expected output as a schema with typed fields."
  - "Validate every response against the schema before it is used."
  - "Retry with the validation error when a response fails, and log the final failure."
reverse:
  - "Pydantic classes passed to a structured output client."
  - "Guardrails RAIL or spec files that define the expected output schema."
packages:
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
  - id: "guardrails"
    name: "Guardrails AI"
    url: "https://github.com/guardrails-ai/guardrails"
tools: []
examples: []
---
