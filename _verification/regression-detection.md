---
title: "Regression detection"
code: "V1051.002"
slug: "regression-detection"
technique: "Past discussion check"
technique_id: "V1051"
technique_slug: "past-discussion-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Raise severity when a change reintroduces a previously fixed problem."
repos: 0
craft:
  - "Record each fixed issue with its code location and the pull request that fixed it."
  - "Check each new finding against fixed issues in the same area of code."
  - "Raise severity when the new change matches a fixed issue."
reverse:
  - "Records of fixed issues that name the pull request that fixed them."
  - "Review comments that say a problem was reintroduced after an earlier fix."
packages:
  - id: "graphiti"
    name: "Graphiti"
    url: "https://github.com/getzep/graphiti"
tools: []
examples: []
---
