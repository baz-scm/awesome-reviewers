---
title: "Merge verdict summary"
code: "V1057.002"
slug: "merge-verdict-summary"
technique: "Merge readiness"
technique_id: "V1057"
technique_slug: "merge-readiness"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "A summary of what is still blocking, with links."
repos: 0
craft:
  - "Write a rule for each blocker, such as a failing check or an unresolved thread."
  - "Post one summary comment that lists each blocker with a link."
  - "Update the same comment on each push instead of posting a new one."
reverse:
  - "A dangerfile.js or dangerfile.ts in the repository root."
  - "Bot comments with a list of blockers that link to failing checks."
  - "A CI job that runs danger on pull requests."
packages:
  - id: "danger"
    name: "Danger JS"
    url: "https://github.com/danger/danger-js"
tools: []
examples: []
---
