---
title: "Dependency risk assessment"
id: "V1018"
slug: "dependency-risk-assessment"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Judges a new dependency beyond known CVEs: maintenance, project security practices and signs of a malicious package."
subtechniques:
  - id: "V1018.001"
    name: "Project health scoring"
    description: "Score a dependency's repository practices (branch protection, signed releases, CI)."
  - id: "V1018.002"
    name: "Malicious package heuristics"
    description: "Scan package contents for install-time scripts, obfuscation and exfiltration."
packages:
  - id: "scorecard"
    name: "OpenSSF Scorecard"
    url: "https://github.com/ossf/scorecard"
  - id: "guarddog"
    name: "GuardDog"
    url: "https://github.com/DataDog/guarddog"
craft:
  - "Run the scan only when a dependency is added or its source changes."
  - "Require a reviewer sign-off below a score threshold rather than failing outright."
reverse:
  - "An ossf/scorecard-action workflow, or guarddog in CI."
---
