---
title: "Malicious package heuristics"
code: "V1018.002"
slug: "malicious-package-heuristics"
technique: "Dependency risk assessment"
technique_id: "V1018"
technique_slug: "dependency-risk-assessment"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Scan package contents for install-time scripts, obfuscation and exfiltration."
repos: 0
craft:
  - "Run a package heuristic scan on each new dependency before its first install."
  - "Check install-time scripts, obfuscated code and network calls in the package contents."
  - "Hold the change until a reviewer clears any flagged package."
reverse:
  - "A guarddog command or workflow step run on new dependency lines."
  - "A CI job that scans package manifests when they change."
  - "A recorded exception list that names packages cleared by a reviewer."
packages:
  - id: "guarddog"
    name: "GuardDog"
    url: "https://github.com/DataDog/guarddog"
tools: []
examples: []
---
