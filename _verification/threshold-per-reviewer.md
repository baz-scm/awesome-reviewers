---
title: "Threshold per reviewer"
code: "V1049.002"
slug: "threshold-per-reviewer"
technique: "Confidence calibration"
technique_id: "V1049"
technique_slug: "confidence-calibration"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Each reviewer gets its own threshold."
repos: 0
craft:
  - "Give each reviewer its own confidence threshold in its config."
  - "Set each threshold from that reviewer's precision target on the logged outcomes."
  - "Recheck the thresholds when a reviewer's prompt or rules change."
reverse:
  - "A per-reviewer config block with a threshold value."
  - "Reviewer config files that each define a separate minimum confidence."
  - "A changelog entry whenever a threshold changes."
packages: []
tools: []
examples: []
---
