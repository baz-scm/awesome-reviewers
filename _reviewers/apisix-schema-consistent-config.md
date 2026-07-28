---
title: Schema-consistent config
description: When implementing configuration-driven features, make validation/forwarding/runtime
  consumption strictly follow the schema and any shared capability wrapper. Avoid
  plugin-specific special casing for generic capabilities, avoid manual per-branch
  field copying that can silently drop accepted config, and ensure environment-variable
  access uses the project’s...
repository: apache/apisix
label: Configurations
language: Other
comments_count: 7
repository_stars: 16922
---

When implementing configuration-driven features, make validation/forwarding/runtime consumption strictly follow the schema and any shared capability wrapper. Avoid plugin-specific special casing for generic capabilities, avoid manual per-branch field copying that can silently drop accepted config, and ensure environment-variable access uses the project’s standard env abstraction.

Practical rules:
1) Validate against the exact schema object that runtime uses (including wrapper/enrichment).
   - Example (pattern):
     ```lua
     function _M.check_schema(conf, schema_type)
         -- if _M.schema is wrapped, validate against _M.schema
         return core.schema.check(_M.schema, conf)
     end
     ```
2) Don’t introduce user-facing config knobs that actually belong to a shared batch processor (or other generic capability). Prefer passing the value into the shared manager capability, and replicate schema entries across all plugins that use the same capability.
3) Enforce meaningful constraints in the user-facing schema (e.g., minimum values), and ensure “accepted by schema” fields are never silently dropped at runtime.
   - Prefer schema-driven forwarding instead of per-policy hand-copying (so future schema additions don’t get missed).
4) For env-backed defaults, use the project’s env API (e.g., `core.env.get(...)`) and ensure documented defaults are truly available in worker runtime (workers only see env vars declared via the appropriate env directive).

Outcome: configuration is accepted/rejected consistently, validated fields reach the underlying implementation, and env-dependent behavior works reliably across standalone and worker runtimes.