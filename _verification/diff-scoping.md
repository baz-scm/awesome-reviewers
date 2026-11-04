---
title: "Diff scoping"
code: "V1047.001"
slug: "diff-scoping"
technique: "Scope and relevance filtering"
technique_id: "V1047"
technique_slug: "scope-and-relevance-filtering"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Report only on changed lines or their immediate context."
repos: 0
craft:
  - "Drop findings whose file and line are not in the diff hunks."
  - "Keep findings on the changed lines and the lines directly around them."
  - "Run the filter before any comment is posted to the pull request."
reverse:
  - "A reviewdog step with filter-mode set to diff_context or added."
  - "Review bot configuration that limits comments to changed lines."
packages:
  - id: "reviewdog"
    name: "reviewdog"
    url: "https://github.com/reviewdog/reviewdog"
tools: []
examples: []
---
