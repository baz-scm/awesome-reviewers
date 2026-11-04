---
title: "Targeted confirmation"
code: "V1062.002"
slug: "targeted-confirmation"
technique: "Exposure verification"
technique_id: "V1062"
technique_slug: "exposure-verification"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Send a request that demonstrates the weakness on a test deployment."
repos: 0
craft:
  - "Select templates that match each exposed service found in discovery."
  - "Run the templates only against non-production hosts."
  - "Record the request and response that confirmed each finding."
reverse:
  - "A nuclei step in a scheduled workflow that passes a templates directory or -t flags."
  - "A ZAP baseline or API scan job pointed at a staging URL."
packages:
  - id: "nuclei"
    name: "Nuclei"
    url: "https://github.com/projectdiscovery/nuclei"
  - id: "zap"
    name: "ZAP"
    url: "https://github.com/zaproxy/zaproxy"
tools: []
examples: []
---
