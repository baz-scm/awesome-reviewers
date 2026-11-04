---
title: "Production error investigation"
id: "V1064"
slug: "production-error-investigation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Investigates production errors from observability data, finds the responsible code and proposes a fix with a regression test."
subtechniques:
  - id: "V1064.001"
    name: "Error-to-code mapping"
    description: "Map a stack trace or log pattern to the commit and lines responsible."
  - id: "V1064.002"
    name: "Automated fix proposal"
    description: "Open a change with the fix and a test that reproduces the error."
packages:
  - id: "holmesgpt"
    name: "HolmesGPT"
    url: "https://github.com/HolmesGPT/holmesgpt"
  - id: "k8sgpt"
    name: "K8sGPT"
    url: "https://github.com/k8sgpt-ai/k8sgpt"
  - id: "openhands"
    name: "OpenHands"
    url: "https://github.com/OpenHands/OpenHands"
craft:
  - "Connect the agent to logs, traces and the repository read-only."
  - "Require a reproduction before any fix."
  - "Route fixes through the same review as human changes."
reverse:
  - "Observability integrations and incident runbooks in the repository."
---
