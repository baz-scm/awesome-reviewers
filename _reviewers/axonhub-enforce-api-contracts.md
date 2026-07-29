---
title: Enforce API Contracts
description: 'When designing or extending APIs, ensure the request/response schema
  and behavior strictly preserve invariants and provider compatibility.


  Apply these rules:'
repository: looplj/axonhub
label: API
language: Go
comments_count: 5
repository_stars: 4808
---

When designing or extending APIs, ensure the request/response schema and behavior strictly preserve invariants and provider compatibility.

Apply these rules:
1) Don’t expose unsafe state transitions
- If a field (e.g., status) must be controlled by an internal state machine, do not add GraphQL mutations/resolvers that allow clients to set it directly—even if the input object contains the field.

2) Use explicit, strongly-typed API models for configuration/mappings
- Prefer dedicated GraphQL types/inputs over generic JSON scalars for mapping objects.
- Validate invariants at the API boundary (e.g., duplicate keys) and ensure the field is reliably returned/persisted (avoid “saving others then dropping mapping” scenarios).

Example (schema shape for typed mappings):
```graphql
input ReasoningEffortMappingInput {
  from: String!
  to: String!
}

type ReasoningEffortMapping {
  from: String!
  to: String!
}

input UpdateChatSettingsInput {
  reasoningEffortMapping: [ReasoningEffortMappingInput!]
}
```

3) Preserve the intended API lifecycle across fallback paths
- If you add auto-aggregation or fallback handling, do not accidentally bypass required middleware phases. Streaming-phase hooks should still execute when the stream is processed.

4) Match third-party spec requirements exactly and guard provider-specific behaviors
- Include fields even when they are zero if the provider spec requires them.
- Apply provider-specific selectors/decorators only when the negotiated API format supports them (use an explicit condition/guard).
