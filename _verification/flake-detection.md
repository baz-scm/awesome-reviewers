---
title: "Flake detection"
code: "V1070.001"
slug: "flake-detection"
technique: "CI failure analysis"
technique_id: "V1070"
technique_slug: "ci-failure-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Re-run and compare to tell flaky tests from real failures."
repos: 0
craft:
  - "Re-run each failing test a fixed number of times on the same commit."
  - "Label a test flaky when it both passes and fails on that commit."
  - "Open an issue for each flaky test and quarantine it until fixed."
reverse:
  - "A quarantine list or skip marker with an issue link for each flaky test."
  - "CI retry settings for specific tests or jobs."
  - "Test result uploads that record pass and fail per run."
packages: []
tools: []
examples: []
---
