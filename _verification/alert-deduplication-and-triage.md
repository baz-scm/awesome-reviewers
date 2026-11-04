---
title: "Alert deduplication and triage"
id: "V1065"
slug: "alert-deduplication-and-triage"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Groups related production alerts and errors and ranks them so investigation starts with the most impactful."
subtechniques:
  - id: "V1065.001"
    name: "Alert correlation"
    description: "Group alerts by fingerprint, service and time window."
  - id: "V1065.002"
    name: "Impact ranking"
    description: "Rank by users affected, frequency and recency."
packages:
  - id: "keep"
    name: "Keep"
    url: "https://github.com/keephq/keep"
  - id: "hdbscan"
    name: "HDBSCAN"
    url: "https://github.com/scikit-learn-contrib/hdbscan"
craft:
  - "Fingerprint errors by normalised stack trace."
  - "Correlate within a time window per service."
  - "Rank before routing to people or agents."
reverse:
  - "Alert routing and grouping rules in monitoring config."
---
