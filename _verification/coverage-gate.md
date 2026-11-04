---
title: "Coverage gate"
code: "V1019.004"
slug: "coverage-gate"
technique: "Unit and integration tests"
technique_id: "V1019"
technique_slug: "unit-and-integration-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Fail when coverage of changed lines drops below a threshold."
repos: 0
craft:
  - "Measure line coverage for the files changed in the pull request."
  - "Set a minimum percentage for the changed lines and fail the job below it."
  - "Upload the coverage report as a CI artifact for review."
reverse:
  - "A coverage threshold setting in the test config, such as fail_under or coverageThreshold."
  - "A CI step that compares coverage on changed lines to a minimum."
  - "A coverage report uploaded as a CI artifact or to a coverage service."
packages: []
tools: []
examples: []
---
