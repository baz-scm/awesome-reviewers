---
title: Use exec-form commands
description: When configuring container commands (e.g., Docker Compose), pass commands
  in exec/array form for any arguments that include secrets or externally provided
  values. This prevents shell parsing/whitespace issues and reduces the risk of injection
  via malformed values (including empty credentials).
repository: infiniflow/ragflow
label: Security
language: Yaml
comments_count: 1
repository_stars: 80174
---

When configuring container commands (e.g., Docker Compose), pass commands in exec/array form for any arguments that include secrets or externally provided values. This prevents shell parsing/whitespace issues and reduces the risk of injection via malformed values (including empty credentials).

Example (safe):
```yaml
services:
  redis:
    image: valkey/valkey:8
    command: [
      "redis-server",
      "--requirepass", "${REDIS_PASSWORD}",
      "--maxmemory", "128mb",
      "--maxmemory-policy", "allkeys-lru"
    ]
```

Avoid string-form commands that rely on implicit parsing:
```yaml
# Not recommended for secrets/external values
command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 128mb
```