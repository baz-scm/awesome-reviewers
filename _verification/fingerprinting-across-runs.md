---
title: "Fingerprinting across runs"
code: "V1045.003"
slug: "fingerprinting-across-runs"
technique: "Finding deduplication"
technique_id: "V1045"
technique_slug: "finding-deduplication"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Stable fingerprints so a finding is recognised on the next commit."
repos: 0
craft:
  - "Compute a fingerprint from the rule ID, file path and normalised code, not the line number."
  - "Store the fingerprint on each finding in the output."
  - "Match new findings to the previous run's fingerprints before reporting them."
reverse:
  - "SARIF results that carry a partialFingerprints object."
  - "A findings table or file keyed by fingerprint."
  - "Normalisation code that strips whitespace before hashing."
packages: []
tools: []
examples: []
---
