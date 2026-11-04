---
title: "Instruction updates from feedback"
code: "V1068.002"
slug: "instruction-updates-from-feedback"
technique: "Reviewer optimization"
technique_id: "V1068"
technique_slug: "reviewer-optimization"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Update reviewer instructions from accepted and rejected findings."
repos: 0
craft:
  - "Record each accepted and rejected finding with the instruction it came from."
  - "Feed rejected findings back as critique of the instruction text."
  - "Review each instruction change like a code change before merge."
reverse:
  - "A feedback log that stores accepted and rejected findings per instruction."
  - "Pull requests that edit reviewer instruction files with a feedback reference."
  - "Instruction files with a changelog or version history."
packages:
  - id: "textgrad"
    name: "TextGrad"
    url: "https://github.com/zou-group/textgrad"
tools: []
examples: []
---
