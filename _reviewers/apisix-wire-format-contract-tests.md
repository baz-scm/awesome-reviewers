---
title: Wire-Format Contract Tests
description: When implementing or modifying any API-facing behavior (endpoint URL
  construction, request/response mappings, routing encodings, capability expansion),
  treat the final wire format as the contract. Prevent silent mismatches by combining
  schema validation, explicit documentation of any byte-exact normalization rules,
  and end-to-end tests that assert the exact...
repository: apache/apisix
label: API
language: Other
comments_count: 4
repository_stars: 16922
---

When implementing or modifying any API-facing behavior (endpoint URL construction, request/response mappings, routing encodings, capability expansion), treat the final wire format as the contract. Prevent silent mismatches by combining schema validation, explicit documentation of any byte-exact normalization rules, and end-to-end tests that assert the exact observable output.

Apply these rules:
- Validate early & fail loudly: if a required endpoint/path/query component is missing or cannot be represented (e.g., Azure deployment root vs deployment+embeddings path), reject in schema/checks instead of letting code build the wrong URL.
- Add end-to-end assertions: if mapping/flattening changes how a client-facing redirect URL/query/body is formed, test the real runtime output (not only schema).
- Document byte-exact formatting: if you normalize encodings/casing in a way that affects matching (e.g., kept “%2F” becomes upper-case), document what authors must write.
- Preserve request pass-through semantics: avoid unintentionally narrowing what fields are forwarded; if behavior must change, make it explicit and test it.

Example pattern (Azure-like capability wiring + runtime validation):
- Schema: reject endpoints that don’t include the required deployment path.
- Capability default: avoid “dead” default paths.
- E2E: call the route using an Azure-shaped endpoint and assert the final request lands on the deployment path including the required query params (e.g., `.../deployments/{deployment}/embeddings?api-version=...`).