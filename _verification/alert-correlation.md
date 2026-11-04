---
title: "Alert correlation"
code: "V1065.001"
slug: "alert-correlation"
technique: "Alert deduplication and triage"
technique_id: "V1065"
technique_slug: "alert-deduplication-and-triage"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Group alerts by fingerprint, service and time window."
repos: 0
craft:
  - "Compute a fingerprint for each alert from its service, error type and normalised stack trace."
  - "Group alerts with the same fingerprint that arrive within the same time window."
  - "Keep one open incident per group and count the repeats."
reverse:
  - "Alert routing config that groups by service with group_wait and group_interval set."
  - "Deduplication or grouping rules in the monitoring config, keyed on a fingerprint field."
packages:
  - id: "keep"
    name: "Keep"
    url: "https://github.com/keephq/keep"
tools: []
examples: []
---
