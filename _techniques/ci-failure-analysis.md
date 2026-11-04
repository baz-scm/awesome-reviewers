---
title: "CI failure analysis"
code: "V1070"
slug: "ci-failure-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Reads failing CI runs, separates real failures from flaky ones, and maps each to the job, step and change that caused it."
subtechniques:
  - id: "V1070.001"
    name: "Flake detection"
    slug: "flake-detection"
    description: "Re-run and compare to tell flaky tests from real failures."
  - id: "V1070.002"
    name: "Workflow structure analysis"
    slug: "workflow-structure-analysis"
    description: "Map jobs and steps to the checks they run (the scanner behind this site does this)."
---
