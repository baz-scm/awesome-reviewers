---
title: "Behavioural questions"
code: "V1040.002"
slug: "behavioural-questions"
technique: "Review question checklists"
technique_id: "V1040"
technique_slug: "review-question-checklists"
tactic: "Code review"
tactic_id: "VA06"
description: "Questions about what changes for users and callers."
repos: 0
craft:
  - "Ask what changes for end users once the change ships."
  - "Ask which callers see a different return value, error or default."
  - "Ask whether the change needs a changelog entry or a migration note."
reverse:
  - "A pull request template section for user-visible or breaking changes."
  - "CHANGELOG.md entries or migration notes added in the same pull requests."
packages:
  - id: "eng-practices"
    name: "Google engineering practices"
    url: "https://github.com/google/eng-practices"
tools: []
examples: []
---
