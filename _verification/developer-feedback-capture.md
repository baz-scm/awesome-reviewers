---
title: "Developer feedback capture"
id: "V1069"
slug: "developer-feedback-capture"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Records how developers respond to findings (fixed, dismissed, argued) and the sentiment of replies, as the ground truth for every other loop."
subtechniques:
  - id: "V1069.001"
    name: "Outcome tracking"
    description: "Was the finding fixed in a later commit, dismissed or ignored."
  - id: "V1069.002"
    name: "Reply sentiment"
    description: "Classify replies as agreeing, disputing or neutral."
packages:
  - id: "argilla"
    name: "Argilla"
    url: "https://github.com/argilla-io/argilla"
  - id: "label-studio"
    name: "Label Studio"
    url: "https://github.com/HumanSignal/label-studio"
  - id: "vader"
    name: "VADER"
    url: "https://github.com/cjhutto/vaderSentiment"
craft:
  - "Store every finding with its later outcome."
  - "Sample disputed findings for human labelling."
  - "Feed labels to calibration and evaluation."
reverse:
  - "Reactions and replies on bot comments, collected by a webhook."
---
