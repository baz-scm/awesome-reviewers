---
title: "Ticket intent alignment"
code: "V1052"
slug: "ticket-intent-alignment"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Checks a finding or a change against the linked ticket: behaviour the ticket declares intentional is not a bug, and requirements it lists must be present."
subtechniques:
  - id: "V1052.001"
    name: "Intended per ticket"
    slug: "intended-per-ticket"
    description: "Suppress findings for behaviour the ticket explicitly asks for or defers."
  - id: "V1052.002"
    name: "Ticket coverage"
    slug: "ticket-coverage"
    description: "List ticket requirements and check each against the diff."
---
