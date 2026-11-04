---
title: "Functional spec verification"
id: "V1054"
slug: "functional-spec-verification"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Runs the application and checks each functional requirement in a browser, returning met, partially met, not met or unverifiable with screenshot evidence."
subtechniques:
  - id: "V1054.001"
    name: "Browser verification"
    description: "An agent or script performs the flow and checks the outcome."
  - id: "V1054.002"
    name: "Evidence capture"
    description: "Screenshot and annotate each verdict."
packages:
  - id: "browser-use"
    name: "Browser Use"
    url: "https://github.com/browser-use/browser-use"
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
  - id: "deepeval"
    name: "DeepEval"
    url: "https://github.com/confident-ai/deepeval"
craft:
  - "Deploy a preview per PR."
  - "Turn each acceptance criterion into a step and an observable outcome."
  - "Attach screenshots to every verdict, including failures."
reverse:
  - "Preview deployment workflows and acceptance criteria in tickets."
---
