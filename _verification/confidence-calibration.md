---
title: "Confidence calibration"
id: "V1049"
slug: "confidence-calibration"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Maps a reviewer's confidence to the observed rate of accepted findings and sets the posting threshold from that curve."
subtechniques:
  - id: "V1049.001"
    name: "Calibration curve"
    description: "Fit confidence against accepted or rejected outcomes."
  - id: "V1049.002"
    name: "Threshold per reviewer"
    description: "Each reviewer gets its own threshold."
packages:
  - id: "scikit-learn"
    name: "scikit-learn"
    url: "https://github.com/scikit-learn/scikit-learn"
craft:
  - "Log confidence and the human outcome for every posted finding."
  - "Fit a calibration model monthly."
  - "Pick the threshold that meets a target precision."
reverse:
  - "Thumbs up or down reactions collected on bot comments."
---
