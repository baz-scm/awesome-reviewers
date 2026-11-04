---
title: "Finding deduplication"
id: "V1045"
slug: "finding-deduplication"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Merges findings that describe the same problem from different reviewers, files or runs into one."
subtechniques:
  - id: "V1045.001"
    name: "Semantic dedup"
    description: "Cluster findings by embedding similarity and location."
  - id: "V1045.002"
    name: "Consolidation"
    description: "Merge a cluster into one finding that keeps all evidence."
  - id: "V1045.003"
    name: "Fingerprinting across runs"
    description: "Stable fingerprints so a finding is recognised on the next commit."
packages:
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
  - id: "faiss"
    name: "FAISS"
    url: "https://github.com/facebookresearch/faiss"
  - id: "sarif-tools"
    name: "sarif-tools"
    url: "https://github.com/microsoft/sarif-tools"
craft:
  - "Emit findings as SARIF or a common schema with file, line and rule."
  - "Fingerprint by rule, file and normalised code, not line number."
  - "Cluster the remainder by embedding and merge."
reverse:
  - "SARIF partialFingerprints, or a findings table keyed by fingerprint."
---
