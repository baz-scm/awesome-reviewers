---
title: "Minimum versions"
code: "V1024.003"
slug: "minimum-versions"
technique: "Version and platform matrix"
technique_id: "V1024"
technique_slug: "version-and-platform-matrix"
tactic: "Testing"
tactic_id: "VA04"
description: "Test with the lowest declared dependency versions."
repos: 0
craft:
  - "Declare the lowest supported version of each dependency in a constraints file."
  - "Install those minimum versions in a separate CI job."
  - "Run the test suite against that job on each pull request."
reverse:
  - "A constraints or lower-bounds requirements file for minimum versions."
  - "A CI job named for minimum or lowest dependency versions."
  - "Lower bounds in dependency declarations that match the tested versions."
packages: []
tools: []
examples: []
---
