---
title: "Calibration curve"
code: "V1049.001"
slug: "calibration-curve"
technique: "Confidence calibration"
technique_id: "V1049"
technique_slug: "confidence-calibration"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Fit confidence against accepted or rejected outcomes."
repos: 0
craft:
  - "Log each posted finding with its reported confidence and the human outcome."
  - "Fit a calibration curve from the logged pairs on a monthly schedule."
  - "Save the fitted curve and the data it was fitted on with the report."
reverse:
  - "A script that imports calibration_curve from scikit-learn."
  - "A log or table of finding outcomes with confidence values."
  - "A scheduled workflow that refits the curve and stores it."
packages:
  - id: "scikit-learn"
    name: "scikit-learn"
    url: "https://github.com/scikit-learn/scikit-learn"
tools: []
examples: []
---
