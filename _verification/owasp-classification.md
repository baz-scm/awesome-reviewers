---
title: "OWASP classification"
code: "V1038.003"
slug: "owasp-classification"
technique: "Security-focused review"
technique_id: "V1038"
technique_slug: "security-focused-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Tag each finding with an OWASP Top 10 category for routing and reporting."
repos: 0
craft:
  - "Map each finding to one OWASP Top 10 category by its root cause."
  - "Store the category as a label or field in every finding record."
  - "Use the category to route findings to the owning team."
reverse:
  - "OWASP Top 10 category labels on security issues or findings."
  - "A security report template with an OWASP category column."
  - "Scanner rule metadata that names an OWASP category."
packages: []
tools: []
examples: []
---
