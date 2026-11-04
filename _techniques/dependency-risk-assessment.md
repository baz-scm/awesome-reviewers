---
title: "Dependency risk assessment"
code: "V1018"
slug: "dependency-risk-assessment"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Judges a new dependency beyond known CVEs: maintenance, project security practices and signs of a malicious package."
subtechniques:
  - id: "V1018.001"
    name: "Project health scoring"
    slug: "project-health-scoring"
    description: "Score a dependency's repository practices (branch protection, signed releases, CI)."
  - id: "V1018.002"
    name: "Malicious package heuristics"
    slug: "malicious-package-heuristics"
    description: "Scan package contents for install-time scripts, obfuscation and exfiltration."
---
