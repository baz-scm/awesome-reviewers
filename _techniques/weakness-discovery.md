---
title: "Weakness discovery"
code: "V1060"
slug: "weakness-discovery"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "For each entry point, searches for the weakness classes that apply to it: injection, broken access control, SSRF, deserialization, path traversal."
subtechniques:
  - id: "V1060.001"
    name: "Per-surface weakness search"
    slug: "per-surface-weakness-search"
    description: "Apply the weakness classes relevant to each surface category."
  - id: "V1060.002"
    name: "Multi-tenancy isolation"
    slug: "multi-tenancy-isolation"
    description: "Check every query and cache key for tenant scoping."
---
