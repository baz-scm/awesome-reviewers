---
title: "Dynamic security testing"
id: "V1027"
slug: "dynamic-security-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Attacks a running instance: crawls endpoints and sends payloads to confirm injection, misconfiguration and exposure."
subtechniques:
  - id: "V1027.001"
    name: "Baseline scan"
    description: "Passive scan of a deployed preview for headers, cookies and known misconfigurations."
  - id: "V1027.002"
    name: "Template-based checks"
    description: "Targeted requests that confirm a specific vulnerability class."
packages:
  - id: "zap"
    name: "ZAP"
    url: "https://github.com/zaproxy/zaproxy"
  - id: "nuclei"
    name: "Nuclei"
    url: "https://github.com/projectdiscovery/nuclei"
craft:
  - "Run a baseline scan against preview deployments."
  - "Write templates for findings from static analysis so they can be confirmed at runtime."
  - "Run active scans only against disposable environments."
reverse:
  - "zap-baseline or nuclei steps in deployment workflows."
  - "Custom nuclei templates in the repository."
---
