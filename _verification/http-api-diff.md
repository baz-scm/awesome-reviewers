---
title: "HTTP API diff"
code: "V1013.001"
slug: "http-api-diff"
technique: "API compatibility checking"
technique_id: "V1013"
technique_slug: "api-compatibility-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Compare OpenAPI documents for breaking changes, and lint them for style."
repos: 0
craft:
  - "Export the OpenAPI document from the base branch and from the head branch in CI."
  - "Run oasdiff breaking between the two files and fail on breaking changes without a version bump."
  - "Lint the head document with Spectral rules and post the result on the pull request."
reverse:
  - "A CI step that runs oasdiff breaking or oasdiff changelog on OpenAPI files."
  - "A .spectral.yaml or .spectral.yml ruleset in the repository."
packages:
  - id: "oasdiff"
    name: "oasdiff"
    url: "https://github.com/oasdiff/oasdiff"
  - id: "spectral"
    name: "Spectral"
    url: "https://github.com/stoplightio/spectral"
tools: []
examples: []
---
