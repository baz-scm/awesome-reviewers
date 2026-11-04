---
title: "Review question checklists"
id: "V1040"
slug: "review-question-checklists"
tactic: "Code review"
tactic_id: "VA06"
description: "A fixed bank of questions a reviewer must answer for a kind of change, ranked so the most relevant ones are asked first."
subtechniques:
  - id: "V1040.001"
    name: "Universal questions"
    description: "Questions that apply to any change: error handling, tests, naming."
  - id: "V1040.002"
    name: "Behavioural questions"
    description: "Questions about what changes for users and callers."
  - id: "V1040.003"
    name: "Security requirement checklists"
    description: "Verification requirements per area from a standard such as OWASP ASVS."
packages:
  - id: "asvs"
    name: "OWASP ASVS"
    url: "https://github.com/OWASP/ASVS"
  - id: "eng-practices"
    name: "Google engineering practices"
    url: "https://github.com/google/eng-practices"
  - id: "rerankers"
    name: "rerankers"
    url: "https://github.com/AnswerDotAI/rerankers"
craft:
  - "Start from a published checklist and keep only questions your reviews actually raise."
  - "Tag each question with the kinds of change it applies to."
  - "Rank by relevance to the diff and ask the top few."
reverse:
  - "PR templates with checkbox lists, or review guidelines in CONTRIBUTING.md."
---
