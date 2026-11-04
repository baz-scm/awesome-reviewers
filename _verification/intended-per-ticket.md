---
title: "Intended per ticket"
code: "V1052.001"
slug: "intended-per-ticket"
technique: "Ticket intent alignment"
technique_id: "V1052"
technique_slug: "ticket-intent-alignment"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Suppress findings for behaviour the ticket explicitly asks for or defers."
repos: 0
craft:
  - "Link each pull request to its ticket key in the title or branch name."
  - "Fetch the ticket and read the sections that say the behaviour is intended or deferred."
  - "Suppress a finding only when the ticket states that exact behaviour, and cite the ticket key."
reverse:
  - "Ticket keys such as ABC-123 in branch names or pull request titles."
  - "A suppression record that cites a ticket key."
  - "An issue tracker integration configured for the repository."
packages:
  - id: "jira"
    name: "jira (Python)"
    url: "https://github.com/pycontribs/jira"
tools: []
examples: []
---
