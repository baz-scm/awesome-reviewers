---
title: "Continuous fuzzing"
code: "V1022.002"
slug: "continuous-fuzzing"
technique: "Fuzzing"
technique_id: "V1022"
technique_slug: "fuzzing"
tactic: "Testing"
tactic_id: "VA04"
description: "Run fuzzers continuously (for example OSS-Fuzz) and file crashes as issues."
repos: 0
craft:
  - "Enrol the project in a hosted continuous fuzzing service, such as OSS-Fuzz."
  - "Configure the service build script so it builds every harness."
  - "Set each crash to open an issue in the project tracker."
reverse:
  - "A project.yaml or build script for OSS-Fuzz in the repository."
  - "A CIFuzz step or scheduled workflow that runs fuzzers for a long time."
  - "Issues labelled as fuzzing crashes that the service filed."
packages: []
tools: []
examples: []
---
