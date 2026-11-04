---
title: "Noise budget"
code: "V1048"
slug: "noise-budget"
tactic: "Finding validation"
tactic_id: "VA07"
description: "A fixed cap on how many findings are posted per change, filled in severity order, so the important ones are read."
subtechniques:
  - id: "V1048.001"
    name: "Volume cap"
    slug: "volume-cap"
    description: "At most N comments per review, highest severity first."
  - id: "V1048.002"
    name: "Carried findings"
    slug: "carried-findings"
    description: "Findings that did not fit are kept and offered on the next run instead of dropped."
---
