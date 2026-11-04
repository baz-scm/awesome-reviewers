---
title: "Ticket intent alignment"
id: "V1052"
slug: "ticket-intent-alignment"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Checks a finding or a change against the linked ticket: behaviour the ticket declares intentional is not a bug, and requirements it lists must be present."
subtechniques:
  - id: "V1052.001"
    name: "Intended per ticket"
    description: "Suppress findings for behaviour the ticket explicitly asks for or defers."
  - id: "V1052.002"
    name: "Ticket coverage"
    description: "List ticket requirements and check each against the diff."
packages:
  - id: "jira"
    name: "jira (Python)"
    url: "https://github.com/pycontribs/jira"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
craft:
  - "Link tickets in PR titles or branch names so they can be fetched."
  - "Extract requirements as a structured list."
  - "Match only on explicit statements; treat silence as unknown."
reverse:
  - "Ticket keys in branch names or PR titles, and issue-tracker integrations."
---
