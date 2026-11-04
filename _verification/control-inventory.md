---
title: "Control inventory"
code: "V1061.001"
slug: "control-inventory"
technique: "Mitigation mapping"
technique_id: "V1061"
technique_slug: "mitigation-mapping"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "List the security controls and where they apply."
repos: 0
craft:
  - "List each security control, such as auth middleware or a rate limiter, with its code location."
  - "Record which entry points each control covers."
  - "Keep the inventory in a threat model file that is reviewed with the code."
reverse:
  - "A threagile.yaml or pytm model file in the repository."
  - "Auth middleware, rate limiter or validation modules named in the threat model."
  - "A security section in the docs that lists controls and their files."
packages:
  - id: "threagile"
    name: "Threagile"
    url: "https://github.com/Threagile/threagile"
  - id: "pytm"
    name: "OWASP pytm"
    url: "https://github.com/OWASP/pytm"
tools: []
examples: []
---
