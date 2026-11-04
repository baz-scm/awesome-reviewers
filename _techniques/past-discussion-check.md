---
title: "Past discussion check"
code: "V1051"
slug: "past-discussion-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Compares a finding with earlier review discussions: a repeat of something already decided is suppressed, a regression of a fixed issue is raised."
subtechniques:
  - id: "V1051.001"
    name: "Repeat suppression"
    slug: "repeat-suppression"
    description: "Do not re-raise what a human already dismissed."
  - id: "V1051.002"
    name: "Regression detection"
    slug: "regression-detection"
    description: "Raise severity when a change reintroduces a previously fixed problem."
---
