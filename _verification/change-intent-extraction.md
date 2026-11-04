---
title: "Change intent extraction"
id: "V1032"
slug: "change-intent-extraction"
tactic: "Code review"
tactic_id: "VA06"
description: "States what the change is meant to do, from title, description, commits and linked ticket, so every later check can ask whether a finding is in scope."
subtechniques:
  - id: "V1032.001"
    name: "Change summary"
    description: "Generate a description and per-file walkthrough of the diff."
  - id: "V1032.002"
    name: "Topic grouping"
    description: "Group changed files by topic and rate each topic's importance."
packages:
  - id: "pr-agent"
    name: "PR-Agent"
    url: "https://github.com/The-PR-Agent/pr-agent"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
  - id: "difftastic"
    name: "Difftastic"
    url: "https://github.com/Wilfred/difftastic"
  - id: "gumtree"
    name: "GumTree"
    url: "https://github.com/GumTreeDiff/gumtree"
craft:
  - "Feed title, body, commit messages and linked ticket to a model with a structured output schema."
  - "Use a structural diff so moved code is not reported as new."
  - "Store the intent with the review so findings can be checked against it."
reverse:
  - "A PR description bot or a generated summary section in PR bodies."
---
