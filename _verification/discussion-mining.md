---
title: "Discussion mining"
code: "V1037.001"
slug: "discussion-mining"
technique: "Reviewers learned from past reviews"
technique_id: "V1037"
technique_slug: "reviewers-learned-from-past-reviews"
tactic: "Code review"
tactic_id: "VA06"
description: "Collect resolved review threads with the code they were on."
repos: 0
craft:
  - "Export resolved review threads with the file path, line and diff hunk for each comment."
  - "Keep the thread outcome, such as accepted, changed or dismissed."
  - "Store the exports as JSON with one record per thread."
reverse:
  - "A script that calls the pull request review comments API and writes JSON."
  - "Exported discussion files that keep file paths and diff hunks beside the review tooling."
packages:
  - id: "pygithub"
    name: "PyGithub"
    url: "https://github.com/PyGithub/PyGithub"
tools: []
examples: []
---
