---
title: "Network entry points"
code: "V1059.001"
slug: "network-entry-points"
technique: "Attack surface inventory"
technique_id: "V1059"
technique_slug: "attack-surface-inventory"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "HTTP, gRPC, WebSocket, raw socket and webhook receivers."
repos: 0
craft:
  - "List the HTTP, gRPC, WebSocket and webhook routes from the route tables or API spec."
  - "Record each entry point as an element with its trust boundary in the threat model."
  - "Review the list when routes are added or their authentication changes."
reverse:
  - "An OpenAPI or route file that the threat model mirrors."
  - "A threagile.yaml or pytm model with an entry for each public endpoint."
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
