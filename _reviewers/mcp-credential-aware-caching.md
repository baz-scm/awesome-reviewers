---
title: Credential-Aware Caching
description: When caching heavyweight clients or connections, treat authentication
  identity (tokens/secret_arn/derived ARN) as part of cache correctness—not just cache
  performance.
repository: awslabs/mcp
label: Caching
language: Python
comments_count: 6
repository_stars: 9545
---

When caching heavyweight clients or connections, treat authentication identity (tokens/secret_arn/derived ARN) as part of cache correctness—not just cache performance.

Standards:
1) Separate lifecycle vs performance caches
- Use a distinct “credential lifecycle” signal/state; when credentials expire/are refreshed, invalidate both the lifecycle state and all dependent cached clients/connections.

2) Cache keys must include auth identity
- If a cached connection/client is created under a specific `secret_arn` (or resolved ARN chain), the cache entry must be keyed on that value (or equivalent). Otherwise, different-secret reconnects will overwrite or reuse the wrong live handle.

3) Resolve-and-compare before lookup when identity is derived
- If the effective secret/ARN depends on remote metadata or configuration resolution, resolve it first, then compare against the cached entry; evict/replace if it differs. Do not return early on a cache hit without verifying that the cached entry matches the resolved auth identity.

4) Refresh auth right before use
- Even if other artifacts are long-lived/cached (e.g., OpenAPI specs), compute/inject auth headers/credentials immediately before the network call so they’re always fresh.

5) Keep cache hits truly “offline”
- A valid cache hit should not trigger network calls (e.g., AWS describe) that were previously avoided; defer network/metadata lookups until after a cache miss.

6) Eviction/replace must clean up
- When replacing an entry (due to secret/ARN changes or failed validation), close the old connection/client and remove using the exact key used in `set()`.

Example (pattern):
```python
# Pseudocode: secret_arn-aware cache with resolve-before-lookup
resolved_secret_arn = resolve_secret_arn(config_or_rds_metadata())

cached = conn_cache.get(key_without_secret_id, secret_arn=resolved_secret_arn)
if cached is not None:
    return cached  # cache hit stays correct

# cache miss (or wrong secret): create fresh connection
conn = create_db_connection(secret_arn=resolved_secret_arn)
validate_or_open(conn)  # optional, but if you do it, evict on failure
conn_cache.set(key_without_secret_id, secret_arn=resolved_secret_arn, conn=conn)
return conn
```

Apply these rules to any in-process caching of `boto3` clients, DB connections/pools, or auth-derived resources to prevent stale-credential behavior and resource leaks while preserving the performance benefits of caching.