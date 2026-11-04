---
title: "Scripted flows"
code: "V1020.001"
slug: "scripted-flows"
technique: "End-to-end browser tests"
technique_id: "V1020"
technique_slug: "end-to-end-browser-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Deterministic scripts for critical paths: sign-in, checkout, settings."
repos: 55
craft:
  - "Write one script per critical path, such as sign-in, checkout and settings."
  - "Select elements by role or test id so scripts survive layout changes."
  - "Save traces and screenshots on failure as CI artifacts."
reverse:
  - "A playwright.config.ts or cypress.config.ts file in the repository."
  - "An e2e directory with spec files for sign-in, checkout or settings flows."
packages:
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
  - id: "cypress"
    name: "Cypress"
    url: "https://github.com/cypress-io/cypress"
tools:
  - name: "playwright"
    repos: 55
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "playwright"
    command: "playwright test --ui-port=0"
  - repo: "nousresearch/hermes-agent"
    tool: "playwright"
    command: "playwright test -c e2e/core/playwright.config.ts local-gateway-attach.spec.ts"
  - repo: "microsoft/vscode"
    tool: "playwright"
    command: "playwright test"
  - repo: "n8n-io/n8n"
    tool: "playwright"
    command: "playwright test --project=e2e tests/e2e/building-blocks/ --workers=1 --retries=2 --reporter=list"
  - repo: "langflow-ai/langflow"
    tool: "playwright"
    command: "playwright test $SCAN_SPECS --project=chromium --shard=$EXPR/$EXPR --workers=2 --retries=1"
---
