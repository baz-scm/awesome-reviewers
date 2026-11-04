---
title: "End-to-end browser tests"
id: "V1020"
slug: "end-to-end-browser-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Drives a real browser through user flows to catch breakage across components, routing and the network."
subtechniques:
  - id: "V1020.001"
    name: "Scripted flows"
    description: "Deterministic scripts for critical paths: sign-in, checkout, settings."
  - id: "V1020.002"
    name: "Agent-driven exploration"
    description: "An LLM agent drives the browser from a natural-language description of the flow."
packages:
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
  - id: "cypress"
    name: "Cypress"
    url: "https://github.com/cypress-io/cypress"
  - id: "browser-use"
    name: "Browser Use"
    url: "https://github.com/browser-use/browser-use"
craft:
  - "Cover the few flows that would page someone if broken."
  - "Seed test data per run and use stable selectors (roles, test ids)."
  - "Record traces and screenshots on failure as CI artifacts."
reverse:
  - "playwright.config or cypress.config and an e2e/ directory."
  - "A CI job that starts the app and runs the browser suite."
---
