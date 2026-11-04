---
title: "Production error investigation"
code: "V1064"
slug: "production-error-investigation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Investigates production errors from observability data, finds the responsible code and proposes a fix with a regression test."
subtechniques:
  - id: "V1064.001"
    name: "Error-to-code mapping"
    slug: "error-to-code-mapping"
    description: "Map a stack trace or log pattern to the commit and lines responsible."
  - id: "V1064.002"
    name: "Automated fix proposal"
    slug: "automated-fix-proposal"
    description: "Open a change with the fix and a test that reproduces the error."
---
