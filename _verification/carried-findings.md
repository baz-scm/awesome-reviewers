---
title: "Carried findings"
code: "V1048.002"
slug: "carried-findings"
technique: "Noise budget"
technique_id: "V1048"
technique_slug: "noise-budget"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Findings that did not fit are kept and offered on the next run instead of dropped."
repos: 0
craft:
  - "Save the findings that did not fit under the cap, keyed by the change identifier."
  - "On the next run, offer saved findings that still apply to the current code."
  - "Drop a saved finding once its code is removed or the issue is fixed."
reverse:
  - "A store of deferred findings, such as a file or database table, keyed by pull request."
  - "Bot comments on later runs that cite earlier carried findings."
packages: []
tools: []
examples: []
---
