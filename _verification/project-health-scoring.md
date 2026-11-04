---
title: "Project health scoring"
code: "V1018.001"
slug: "project-health-scoring"
technique: "Dependency risk assessment"
technique_id: "V1018"
technique_slug: "dependency-risk-assessment"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Score a dependency's repository practices (branch protection, signed releases, CI)."
repos: 0
craft:
  - "Run a repository health scan on each new dependency and record the score."
  - "Set a score threshold below which a reviewer must sign off."
  - "Re-run the scan when the dependency is upgraded."
reverse:
  - "A scorecard or ossf/scorecard-action step in a workflow."
  - "A dependency review file that lists scores or required sign-offs."
  - "A written reviewer rule that names the score threshold."
packages:
  - id: "scorecard"
    name: "OpenSSF Scorecard"
    url: "https://github.com/ossf/scorecard"
tools: []
examples: []
---
