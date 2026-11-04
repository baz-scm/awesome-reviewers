---
title: "Risk prioritization"
id: "V1063"
slug: "risk-prioritization"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Orders confirmed weaknesses by exposure, exploit likelihood and impact so fixes start where risk is highest."
subtechniques:
  - id: "V1063.001"
    name: "Decision trees"
    description: "SSVC decisions from exploitation, exposure and impact."
  - id: "V1063.002"
    name: "Likelihood scores"
    description: "EPSS for known vulnerabilities."
packages:
  - id: "ssvc"
    name: "CERT/CC SSVC"
    url: "https://github.com/CERTCC/SSVC"
  - id: "cvss"
    name: "cvss (Python)"
    url: "https://github.com/RedHatProductSecurity/cvss"
craft:
  - "Score exposure from the attack surface inventory."
  - "Combine with likelihood and impact through a fixed decision tree."
  - "Recompute when exposure changes."
reverse:
  - "Vulnerability management dashboards or SECURITY.md response targets."
---
