---
title: "Outcome tracking"
code: "V1069.001"
slug: "outcome-tracking"
technique: "Developer feedback capture"
technique_id: "V1069"
technique_slug: "developer-feedback-capture"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Was the finding fixed in a later commit, dismissed or ignored."
repos: 0
craft:
  - "Store each finding with its ID, file, line and the commit it was raised on."
  - "On each later push, check whether the flagged lines changed and record fixed, dismissed or ignored."
  - "Keep the outcome record for each finding so calibration can use it."
reverse:
  - "A findings table or log file that records each finding's status."
  - "A scheduled job that reads resolved review threads and writes their status back."
packages: []
tools: []
examples: []
---
