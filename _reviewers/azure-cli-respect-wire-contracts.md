---
title: Respect Wire Contracts
description: When calling REST endpoints, ensure the client request/response payload
  exactly matches the endpoint’s wire contract—especially when GET and PUT/PATCH shapes
  differ (nested ARM-canonical vs flat service payload) or when envelope fields must
  be consistent.
repository: Azure/azure-cli
label: API
language: Python
comments_count: 6
repository_stars: 4592
---

When calling REST endpoints, ensure the client request/response payload exactly matches the endpoint’s wire contract—especially when GET and PUT/PATCH shapes differ (nested ARM-canonical vs flat service payload) or when envelope fields must be consistent.

Actionable rules:
- Don’t reuse “generic update” flows when the service rejects properties due to wire-shape differences. If PUT expects a flat body while GET returns nested `properties`, construct the PUT payload explicitly (or use the dedicated create/update operation that matches the PUT contract).
- Ensure field locations match the contract (e.g., `properties.<field>` vs top-level). If your SDK model moved fields under `.properties`, update payload mapping accordingly.
- Keep envelopes consistent across operations (upload vs import): include all fields the API expects (e.g., `serverFarmId`) in every envelope.
- For content typing/discriminators (Docker vs OCI), don’t assume JSON always contains `mediaType`; parse from response `content-type` when possible.
- Don’t rely on SDK escape hatches (like `additional_properties`) once the typed model is migrated.

Example (avoid generic-update for asymmetric shapes):
```py
# Bad: generic-update typically does GET -> modify -> PUT
# but PUT expects flat { latestScan, results } while GET returns
# { properties: { latestScan, results } }, leading to 400 UnsupportedProperties.

# Good: call the endpoint that matches the PUT contract, or build
# the exact PUT payload shape explicitly.
put_payload = {
    "latestScan": command_args.get("latest_scan"),
    "results": command_args.get("results"),
}
# send put_payload directly to the baselineRules/{ruleId} PUT endpoint
```

Use this as a checklist before wiring a new operation or refactoring payload mapping: verify the exact request body shape (nesting + field names) against the endpoint’s spec, and don’t assume the SDK model shape equals the service’s accepted wire shape.