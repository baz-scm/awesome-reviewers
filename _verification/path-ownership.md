---
title: "Path ownership"
code: "V1041.001"
slug: "path-ownership"
technique: "Reviewer routing"
technique_id: "V1041"
technique_slug: "reviewer-routing"
tactic: "Code review"
tactic_id: "VA06"
description: "Route by file path ownership rules."
repos: 0
craft:
  - "List the owners of each top-level directory in CODEOWNERS."
  - "Require review from a listed owner for changes to owned paths."
  - "Update the file when a team or directory changes owner."
reverse:
  - "A CODEOWNERS file at the repository root or under .github."
  - "Branch protection rules that require code owner review."
  - "Review requests on pull requests that name a team for a path."
packages: []
tools: []
examples: []
---
