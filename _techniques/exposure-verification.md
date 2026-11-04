---
title: "Exposure verification"
code: "V1062"
slug: "exposure-verification"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Confirms which weaknesses are reachable from outside: external asset discovery and targeted checks against deployed endpoints."
subtechniques:
  - id: "V1062.001"
    name: "External asset discovery"
    slug: "external-asset-discovery"
    description: "Enumerate domains, subdomains and exposed services."
  - id: "V1062.002"
    name: "Targeted confirmation"
    slug: "targeted-confirmation"
    description: "Send a request that demonstrates the weakness on a test deployment."
---
