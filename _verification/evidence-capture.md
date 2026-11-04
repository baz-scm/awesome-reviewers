---
title: "Evidence capture"
code: "V1054.002"
slug: "evidence-capture"
technique: "Functional spec verification"
technique_id: "V1054"
technique_slug: "functional-spec-verification"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Screenshot and annotate each verdict."
repos: 55
craft:
  - "Take a screenshot at each assertion, including the failing one."
  - "Store the verdict and the criterion text next to each screenshot."
  - "Attach the screenshots to the pull request or to the job artifacts."
reverse:
  - "screenshot: 'only-on-failure' or trace settings in playwright.config."
  - "A CI step that uploads test-results or screenshot folders as artifacts."
packages:
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
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
