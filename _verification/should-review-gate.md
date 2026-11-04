---
title: "Should-review gate"
code: "V1038.001"
slug: "should-review-gate"
technique: "Security-focused review"
technique_id: "V1038"
technique_slug: "security-focused-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Decide from the diff whether a deeper security pass is warranted."
repos: 0
craft:
  - "Define diff triggers for a deeper security pass: new routes, auth code, deserialization, subprocess and SQL."
  - "Run the gate on every pull request before the review is requested."
  - "Record which trigger matched in the review comment."
reverse:
  - "A path or pattern list in CI config that marks security-sensitive files."
  - "A workflow step that comments which security trigger matched."
  - "CODEOWNERS entries for auth or api directories."
packages: []
tools: []
examples: []
---
