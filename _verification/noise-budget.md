---
title: "Noise budget"
id: "V1048"
slug: "noise-budget"
tactic: "Finding validation"
tactic_id: "VA07"
description: "A fixed cap on how many findings are posted per change, filled in severity order, so the important ones are read."
subtechniques:
  - id: "V1048.001"
    name: "Volume cap"
    description: "At most N comments per review, highest severity first."
  - id: "V1048.002"
    name: "Carried findings"
    description: "Findings that did not fit are kept and offered on the next run instead of dropped."
packages:
  - id: "reviewdog"
    name: "reviewdog"
    url: "https://github.com/reviewdog/reviewdog"
  - id: "sarif-tools"
    name: "sarif-tools"
    url: "https://github.com/microsoft/sarif-tools"
craft:
  - "Set the cap from how many comments reviewers actually address."
  - "Sort by severity, then certainty."
  - "Store the overflow and resurface it when the budget allows."
reverse:
  - "Review bot config with a maximum comment count."
---
