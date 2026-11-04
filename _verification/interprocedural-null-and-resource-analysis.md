---
title: "Interprocedural null and resource analysis"
code: "V1014.001"
slug: "interprocedural-null-and-resource-analysis"
technique: "Data and control flow analysis"
technique_id: "V1014"
technique_slug: "data-and-control-flow-analysis"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Report null dereferences and leaks along concrete paths."
repos: 0
craft:
  - "Run Infer on the default branch to record the baseline of null and resource reports."
  - "Run it on each change and report only issues on new paths."
  - "Fix or suppress each report, with a comment that gives the reason."
reverse:
  - "An infer step in CI or a build target that runs the analyzer."
  - "An infer-out directory from a run, or suppression comments on reported lines."
  - "A .inferconfig file in the repository root."
packages:
  - id: "infer"
    name: "Infer"
    url: "https://github.com/meta/infer"
tools: []
examples: []
---
