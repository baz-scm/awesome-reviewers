---
title: "Mitigation mapping"
code: "V1061"
slug: "mitigation-mapping"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Checks whether each weakness is already mitigated by a control (validation, authorization middleware, rate limits) before reporting it."
subtechniques:
  - id: "V1061.001"
    name: "Control inventory"
    slug: "control-inventory"
    description: "List the security controls and where they apply."
  - id: "V1061.002"
    name: "Coverage check"
    slug: "coverage-check"
    description: "Report entry points that bypass the controls."
---
