---
title: "Consolidation"
code: "V1045.002"
slug: "consolidation"
technique: "Finding deduplication"
technique_id: "V1045"
technique_slug: "finding-deduplication"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Merge a cluster into one finding that keeps all evidence."
repos: 0
craft:
  - "Merge each cluster into one finding that lists every source rule, file and run."
  - "Keep the evidence of each merged finding in a locations array."
  - "Keep the original findings linked so reviewers can audit the merge."
reverse:
  - "A sarif-tools merge step or a script that merges SARIF runs."
  - "A SARIF result with multiple locations for one problem."
  - "A merge step between the scanner and the upload step in CI."
packages:
  - id: "sarif-tools"
    name: "sarif-tools"
    url: "https://github.com/microsoft/sarif-tools"
tools: []
examples: []
---
