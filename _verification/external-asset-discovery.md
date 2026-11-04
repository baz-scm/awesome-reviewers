---
title: "External asset discovery"
code: "V1062.001"
slug: "external-asset-discovery"
technique: "Exposure verification"
technique_id: "V1062"
technique_slug: "exposure-verification"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Enumerate domains, subdomains and exposed services."
repos: 0
craft:
  - "Run amass against the organisation's root domains on a fixed schedule."
  - "Record every discovered domain and service in an inventory file."
  - "Diff each run against the previous inventory and flag new assets."
reverse:
  - "A scheduled workflow that calls amass enum or amass intel."
  - "An inventory file or config that lists the root domains for discovery."
packages:
  - id: "amass"
    name: "OWASP Amass"
    url: "https://github.com/owasp-amass/amass"
tools: []
examples: []
---
