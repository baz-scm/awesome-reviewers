---
title: "Breadth survey"
code: "V1034.001"
slug: "breadth-survey"
technique: "Agentic exploration"
technique_id: "V1034"
technique_slug: "agentic-exploration"
tactic: "Code review"
tactic_id: "VA06"
description: "A first pass that lists concerns across the whole diff."
repos: 0
craft:
  - "Give the agent the full diff and a fixed list of review concerns."
  - "Ask for a short list of concerns across all changed files, each with a file and line."
  - "Discard any concern that has no citation before the deeper pass."
reverse:
  - "An agent prompt or task template that lists review concerns."
  - "Review bot comments that cite several files for one concern."
  - "An agent run log that lists concerns before the detailed passes."
packages:
  - id: "openhands"
    name: "OpenHands"
    url: "https://github.com/OpenHands/OpenHands"
tools: []
examples: []
---
