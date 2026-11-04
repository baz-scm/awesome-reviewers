---
title: "Output guardrails"
code: "V1058"
slug: "output-guardrails"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Validates what an automated reviewer or fixer produces before it is posted or committed: schema, policy and safety checks."
subtechniques:
  - id: "V1058.001"
    name: "Schema validation"
    slug: "schema-validation"
    description: "Reject malformed structured output and retry."
  - id: "V1058.002"
    name: "Policy rails"
    slug: "policy-rails"
    description: "Block outputs that leak secrets, change protected files or exceed scope."
---
