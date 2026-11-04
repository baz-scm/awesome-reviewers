---
title: "Pull request rules"
code: "V1004.002"
slug: "pull-request-rules"
technique: "Commit and pull request hygiene"
technique_id: "V1004"
technique_slug: "commit-and-pull-request-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Fail or warn when a PR is too large, lacks a description, or touches files without matching tests or docs."
repos: 0
craft:
  - "Write a Dangerfile that reads PR size, description and labels from the event."
  - "Warn above the agreed size limit and fail when the description is empty."
  - "Require a test or docs file in the diff when source files under a listed path change."
reverse:
  - "A dangerfile.ts or dangerfile.js at the repository root."
  - "A CI job that runs danger on pull_request events."
packages:
  - id: "danger"
    name: "Danger JS"
    url: "https://github.com/danger/danger-js"
tools: []
examples: []
---
