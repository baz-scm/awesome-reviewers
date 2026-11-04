---
title: "Requirement tracing"
code: "V1053.001"
slug: "requirement-tracing"
technique: "Plan and spec traceability"
technique_id: "V1053"
technique_slug: "plan-and-spec-traceability"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Link requirement ids to code and tests."
repos: 0
craft:
  - "Give each requirement in the spec a stable id."
  - "Add that id to the code comment or test name that implements it."
  - "Run the tracing tool in CI and fail on requirements with no link."
reverse:
  - "Requirement ids in spec files that tests and code comments reference."
  - "A specs/ or docs/adr directory with numbered requirement files."
  - "A CI step that runs OpenFastTrace over the spec and source directories."
packages:
  - id: "openfasttrace"
    name: "OpenFastTrace"
    url: "https://github.com/itsallcode/openfasttrace"
tools: []
examples: []
---
