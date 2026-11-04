---
title: "Red-team probing"
code: "V1039.002"
slug: "red-team-probing"
technique: "LLM application security review"
technique_id: "V1039"
technique_slug: "llm-application-security-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Send adversarial prompts to a running application and score the responses."
repos: 0
craft:
  - "Write a suite of adversarial prompts for each prompt-handling path."
  - "Run the suite against a running build in a test environment."
  - "Score each response with fixed rules and fail the job on any policy break."
reverse:
  - "A promptfooconfig.yaml or garak config file in the repository."
  - "A CI job that runs promptfoo or garak against a test deployment."
  - "A test-case file that lists injection and leakage prompts."
packages:
  - id: "garak"
    name: "garak"
    url: "https://github.com/NVIDIA/garak"
  - id: "promptfoo"
    name: "promptfoo"
    url: "https://github.com/promptfoo/promptfoo"
tools: []
examples: []
---
