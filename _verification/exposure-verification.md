---
title: "Exposure verification"
id: "V1062"
slug: "exposure-verification"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Confirms which weaknesses are reachable from outside: external asset discovery and targeted checks against deployed endpoints."
subtechniques:
  - id: "V1062.001"
    name: "External asset discovery"
    description: "Enumerate domains, subdomains and exposed services."
  - id: "V1062.002"
    name: "Targeted confirmation"
    description: "Send a request that demonstrates the weakness on a test deployment."
packages:
  - id: "amass"
    name: "OWASP Amass"
    url: "https://github.com/owasp-amass/amass"
  - id: "nuclei"
    name: "Nuclei"
    url: "https://github.com/projectdiscovery/nuclei"
  - id: "zap"
    name: "ZAP"
    url: "https://github.com/zaproxy/zaproxy"
craft:
  - "Discover assets on a schedule."
  - "Map findings to exposed assets."
  - "Confirm with targeted templates against non-production environments."
reverse:
  - "Scheduled scan workflows and nuclei templates."
---
