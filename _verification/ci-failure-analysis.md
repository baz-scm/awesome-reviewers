---
title: "CI failure analysis"
id: "V1070"
slug: "ci-failure-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Reads failing CI runs, separates real failures from flaky ones, and maps each to the job, step and change that caused it."
subtechniques:
  - id: "V1070.001"
    name: "Flake detection"
    description: "Re-run and compare to tell flaky tests from real failures."
  - id: "V1070.002"
    name: "Workflow structure analysis"
    description: "Map jobs and steps to the checks they run (the scanner behind this site does this)."
packages:
  - id: "actionlint"
    name: "actionlint"
    url: "https://github.com/rhysd/actionlint"
  - id: "pytest"
    name: "pytest"
    url: "https://github.com/pytest-dev/pytest"
craft:
  - "Record test outcomes per run, not just the job status."
  - "Quarantine tests that fail and pass on the same commit, and file an issue."
  - "Never skip a test to get a green run."
reverse:
  - "Retry settings, flaky markers and test result uploads in CI."
---
