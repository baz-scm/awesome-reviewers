---
title: "Call-chain investigation"
code: "V1038.002"
slug: "call-chain-investigation"
technique: "Security-focused review"
technique_id: "V1038"
technique_slug: "security-focused-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Follow user input from entry point to sink with a model, file by file."
repos: 0
craft:
  - "Start from each route or handler that takes user input."
  - "Follow the input file by file to the sink, such as a query, shell call or file path."
  - "Report a finding only with a concrete input that reaches the sink."
reverse:
  - "A script or config that runs vulnhuntr against the web app's entry points."
  - "Security review comments that cite a call chain from route to sink."
  - "Test cases with a malicious input for each reported sink."
packages:
  - id: "vulnhuntr"
    name: "Vulnhuntr"
    url: "https://github.com/protectai/vulnhuntr"
tools: []
examples: []
---
