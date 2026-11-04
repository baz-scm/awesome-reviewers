---
title: "Automated fix proposal"
code: "V1064.002"
slug: "automated-fix-proposal"
technique: "Production error investigation"
technique_id: "V1064"
technique_slug: "production-error-investigation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Open a change with the fix and a test that reproduces the error."
repos: 0
craft:
  - "Require a reproduction of the production error before any fix is drafted."
  - "Open the fix as a pull request with a test that reproduces the error."
  - "Route the pull request through the same review and checks as human changes."
reverse:
  - "Pull requests from an automated author that link an error or incident."
  - "A regression test in the fix pull request that fails before the fix."
  - "A workflow that opens pull requests from an error report."
packages:
  - id: "swe-agent"
    name: "SWE-agent"
    url: "https://github.com/SWE-agent/SWE-agent"
tools: []
examples: []
---
