---
title: "Rule file review"
code: "V1036.001"
slug: "rule-file-review"
technique: "Convention and guideline review"
technique_id: "V1036"
technique_slug: "convention-and-guideline-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Apply the rules in AGENTS.md, CLAUDE.md or CONTRIBUTING.md to the diff."
repos: 0
craft:
  - "Collect the rules from AGENTS.md or CONTRIBUTING.md into one numbered list."
  - "Give each rule an ID or heading so a finding can cite it."
  - "Apply to each changed file only the rules whose scope covers its path."
reverse:
  - "An AGENTS.md or CONTRIBUTING.md at the repository root with numbered coding rules."
  - "Review prompts or bot configuration that reference a rules file path."
packages: []
tools: []
examples: []
---
