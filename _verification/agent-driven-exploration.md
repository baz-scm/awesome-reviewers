---
title: "Agent-driven exploration"
code: "V1020.002"
slug: "agent-driven-exploration"
technique: "End-to-end browser tests"
technique_id: "V1020"
technique_slug: "end-to-end-browser-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "An LLM agent drives the browser from a natural-language description of the flow."
repos: 0
craft:
  - "Write each flow as a short natural-language goal with the expected end state."
  - "Run the agent against a test account and seeded data, never production data."
  - "Keep the agent's steps and the final page state as the result of each run."
reverse:
  - "Flow description files, such as markdown or YAML goals, in an e2e or agent directory."
  - "Agent run logs or recorded step transcripts attached to CI results."
packages:
  - id: "browser-use"
    name: "Browser Use"
    url: "https://github.com/browser-use/browser-use"
tools: []
examples: []
---
