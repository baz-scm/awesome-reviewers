---
title: "Dynamic security testing"
code: "V1027"
slug: "dynamic-security-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Attacks a running instance: crawls endpoints and sends payloads to confirm injection, misconfiguration and exposure."
subtechniques:
  - id: "V1027.001"
    name: "Baseline scan"
    slug: "baseline-scan"
    description: "Passive scan of a deployed preview for headers, cookies and known misconfigurations."
  - id: "V1027.002"
    name: "Template-based checks"
    slug: "template-based-checks"
    description: "Targeted requests that confirm a specific vulnerability class."
---
