---
title: "Baseline scan"
code: "V1027.001"
slug: "baseline-scan"
technique: "Dynamic security testing"
technique_id: "V1027"
technique_slug: "dynamic-security-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Passive scan of a deployed preview for headers, cookies and known misconfigurations."
repos: 0
craft:
  - "Deploy each pull request to a preview environment."
  - "Run a passive baseline scan against the preview URL."
  - "Record the findings and fail only on new header or cookie problems."
reverse:
  - "A zap-baseline step in a preview or deployment workflow."
  - "A ZAP rules file that suppresses accepted alerts."
  - "A preview URL passed to the scanner in the workflow."
packages:
  - id: "zap"
    name: "ZAP"
    url: "https://github.com/zaproxy/zaproxy"
tools: []
examples: []
---
