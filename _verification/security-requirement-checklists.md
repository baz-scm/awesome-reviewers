---
title: "Security requirement checklists"
code: "V1040.003"
slug: "security-requirement-checklists"
technique: "Review question checklists"
technique_id: "V1040"
technique_slug: "review-question-checklists"
tactic: "Code review"
tactic_id: "VA06"
description: "Verification requirements per area from a standard such as OWASP ASVS."
repos: 0
craft:
  - "Pick the ASVS chapters that match the code area, such as authentication or session handling."
  - "Turn each chosen requirement into a yes or no question for the reviewer."
  - "Record the requirement ID in the review comment when a change fails it."
reverse:
  - "A security review checklist in the repository that cites ASVS requirement IDs such as V2.1.1."
  - "Pull request templates with security checkboxes that link to ASVS."
packages:
  - id: "asvs"
    name: "OWASP ASVS"
    url: "https://github.com/OWASP/ASVS"
tools: []
examples: []
---
