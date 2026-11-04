---
title: "Infrastructure and configuration"
code: "V1059.004"
slug: "infrastructure-and-configuration"
technique: "Attack surface inventory"
technique_id: "V1059"
technique_slug: "attack-surface-inventory"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Infrastructure as code, secrets management, caching and edge routing."
repos: 0
craft:
  - "List the infrastructure as code files, secrets stores, caches and edge routing rules."
  - "Model each one as a component with its trust boundary and data flow."
  - "Update the model when a new service, bucket or route is added."
reverse:
  - "Terraform, Helm or CloudFormation files whose components also appear in the threat model."
  - "A secrets manager reference or CDN routing configuration listed in the threat model file."
packages:
  - id: "pytm"
    name: "OWASP pytm"
    url: "https://github.com/OWASP/pytm"
  - id: "threagile"
    name: "Threagile"
    url: "https://github.com/Threagile/threagile"
  - id: "threat-dragon"
    name: "OWASP Threat Dragon"
    url: "https://github.com/OWASP/threat-dragon"
tools: []
examples: []
---
