---
title: "Token clone detection"
code: "V1011.001"
slug: "token-clone-detection"
technique: "Duplicate code detection"
technique_id: "V1011"
technique_slug: "duplicate-code-detection"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Report token-identical or near-identical blocks above a size threshold."
repos: 0
craft:
  - "Run jscpd or PMD CPD with a minimum token count that fits the language."
  - "Exclude tests, generated code and vendored directories from the scan."
  - "Fail the check only on clones that the change introduces."
reverse:
  - ".jscpd.json or a cpd task in the build file."
  - "Exclude patterns for generated, vendored or test paths in the detector config."
  - "Clone reports in CI output with a token threshold setting."
packages:
  - id: "jscpd"
    name: "jscpd"
    url: "https://github.com/kucherenko/jscpd"
  - id: "pmd"
    name: "PMD (CPD)"
    url: "https://github.com/pmd/pmd"
tools: []
examples: []
---
