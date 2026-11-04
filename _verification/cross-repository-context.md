---
title: "Cross-repository context"
code: "V1033.003"
slug: "cross-repository-context"
technique: "Review context retrieval"
technique_id: "V1033"
technique_slug: "review-context-retrieval"
tactic: "Code review"
tactic_id: "VA06"
description: "Look up how other services call or are called by the changed code."
repos: 0
craft:
  - "Maintain a list of the services this code calls and the services that call it."
  - "Look up callers in other repositories for each changed public interface."
  - "Attach the cross-repository callers to the review context with their file paths."
reverse:
  - "A service dependency map or a shared API contract file, such as OpenAPI, kept across repositories."
  - "Review context that lists callers from repositories other than the one under review."
packages: []
tools: []
examples: []
---
