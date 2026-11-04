---
title: "Plan and spec traceability"
id: "V1053"
slug: "plan-and-spec-traceability"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Checks each requirement in a plan or specification against the implementation: done in this change, done elsewhere, or not started, with gaps graded by severity."
subtechniques:
  - id: "V1053.001"
    name: "Requirement tracing"
    description: "Link requirement ids to code and tests."
  - id: "V1053.002"
    name: "Gap analysis"
    description: "Report where the implementation departs from the plan's intent."
packages:
  - id: "spec-kit"
    name: "Spec Kit"
    url: "https://github.com/github/spec-kit"
  - id: "openfasttrace"
    name: "OpenFastTrace"
    url: "https://github.com/itsallcode/openfasttrace"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
craft:
  - "Write specs with stable requirement ids."
  - "Reference the ids in code comments or tests."
  - "Report untraced requirements and code with no requirement."
reverse:
  - "specs/ or docs/adr directories, requirement ids in tests."
---
