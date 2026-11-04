---
title: "Mitigation mapping"
id: "V1061"
slug: "mitigation-mapping"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Checks whether each weakness is already mitigated by a control (validation, authorization middleware, rate limits) before reporting it."
subtechniques:
  - id: "V1061.001"
    name: "Control inventory"
    description: "List the security controls and where they apply."
  - id: "V1061.002"
    name: "Coverage check"
    description: "Report entry points that bypass the controls."
packages:
  - id: "threagile"
    name: "Threagile"
    url: "https://github.com/Threagile/threagile"
  - id: "pytm"
    name: "OWASP pytm"
    url: "https://github.com/OWASP/pytm"
craft:
  - "List controls as code locations (middleware, decorators, gateways)."
  - "Check each entry point passes through them."
  - "Report only unmitigated weaknesses."
reverse:
  - "Auth middleware, rate limiter and validation layers in the code."
---
