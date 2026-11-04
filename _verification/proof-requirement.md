---
title: "Proof requirement"
code: "V1042.002"
slug: "proof-requirement"
technique: "Evidence-backed verification"
technique_id: "V1042"
technique_slug: "evidence-backed-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Drop findings that cite no line, input or behaviour."
repos: 0
craft:
  - "Reject any finding that does not name a file and line."
  - "Require each finding to state the input or sequence that triggers the behaviour."
  - "Drop findings whose claim cannot be tied to code in the diff."
reverse:
  - "Review tool templates or schemas that require a line reference and a triggering input."
  - "Bot comments that give a file, line and triggering input for each finding."
packages: []
tools: []
examples: []
---
