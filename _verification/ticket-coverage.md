---
title: "Ticket coverage"
code: "V1052.002"
slug: "ticket-coverage"
technique: "Ticket intent alignment"
technique_id: "V1052"
technique_slug: "ticket-intent-alignment"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "List ticket requirements and check each against the diff."
repos: 0
craft:
  - "Extract each requirement from the ticket into a numbered list with a fixed schema."
  - "Check each requirement against the diff and record the file and line that meets it."
  - "Mark a requirement as unknown when the diff does not state it either way."
reverse:
  - "A requirements checklist field in the pull request template."
  - "A structured output schema for requirement extraction in the code."
  - "Coverage results posted as a checklist comment on the pull request."
packages:
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
  - id: "jira"
    name: "jira (Python)"
    url: "https://github.com/pycontribs/jira"
tools: []
examples: []
---
