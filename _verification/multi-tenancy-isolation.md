---
title: "Multi-tenancy isolation"
code: "V1060.002"
slug: "multi-tenancy-isolation"
technique: "Weakness discovery"
technique_id: "V1060"
technique_slug: "weakness-discovery"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Check every query and cache key for tenant scoping."
repos: 0
craft:
  - "List every query, cache key and queue topic that holds tenant data."
  - "Confirm each one includes the tenant identifier taken from the request context."
  - "Add a test that reads one tenant's data while authenticated as another and expects no result."
reverse:
  - "Query helpers that take a tenant_id or tenant argument."
  - "Cache key builders that prefix keys with a tenant identifier."
  - "Cross-tenant access tests in the test suite."
packages: []
tools: []
examples: []
---
