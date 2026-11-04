---
title: "Tiered depth"
code: "V1034.003"
slug: "tiered-depth"
technique: "Agentic exploration"
technique_id: "V1034"
technique_slug: "agentic-exploration"
tactic: "Code review"
tactic_id: "VA06"
description: "Route small or low-risk changes to a shallow pass and risky ones to deep exploration."
repos: 0
craft:
  - "Define risk signals from the diff, such as touched paths, change size and touched APIs."
  - "Send low-risk changes to the shallow pass and risky changes to the deep pass."
  - "Log which depth ran for each pull request."
reverse:
  - "A routing rule or config file that selects review depth by path or size."
  - "A CI step that logs which review depth ran for each pull request."
  - "Routing thresholds stored next to the review workflow."
packages:
  - id: "routellm"
    name: "RouteLLM"
    url: "https://github.com/lm-sys/RouteLLM"
tools: []
examples: []
---
