---
title: "Browser verification"
code: "V1054.001"
slug: "browser-verification"
technique: "Functional spec verification"
technique_id: "V1054"
technique_slug: "functional-spec-verification"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "An agent or script performs the flow and checks the outcome."
repos: 55
craft:
  - "Turn each acceptance criterion into a sequence of browser steps."
  - "Run the steps against the preview deployment for the pull request."
  - "Assert the observable outcome, such as visible text or a URL change, for each step."
reverse:
  - "Playwright test files that open the preview URL from an environment variable."
  - "A preview deployment workflow that passes its URL to the test job."
packages:
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
  - id: "browser-use"
    name: "Browser Use"
    url: "https://github.com/browser-use/browser-use"
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
