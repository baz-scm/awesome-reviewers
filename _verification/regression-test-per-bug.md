---
title: "Regression test per bug"
code: "V1019.003"
slug: "regression-test-per-bug"
technique: "Unit and integration tests"
technique_id: "V1019"
technique_slug: "unit-and-integration-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Every fixed bug gets a test that failed before the fix."
repos: 0
craft:
  - "Write a test that reproduces the bug and run it before the fix."
  - "Confirm the test fails on the old commit and passes after the fix."
  - "Name the test after the bug or link it to the bug report."
reverse:
  - "Test names or comments that cite an issue number for a fixed bug."
  - "Pull requests with a fix that also add a test case."
  - "A regression test directory or marker, such as tests/regression."
packages: []
tools: []
examples: []
---
