---
title: "Asynchronous entry points"
code: "V1059.002"
slug: "asynchronous-entry-points"
technique: "Attack surface inventory"
technique_id: "V1059"
technique_slug: "attack-surface-inventory"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Queue consumers and scheduled jobs that act on external data."
repos: 0
craft:
  - "List each queue consumer, cron job and scheduled task that reads external data."
  - "Mark queues that receive data from outside the service as trust boundaries."
  - "Keep the asynchronous entries in the threat model next to the network entry points."
reverse:
  - "Queue or scheduler configuration files, such as cron definitions or worker manifests."
  - "A threat model file with asynchronous entries marked as untrusted input."
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
