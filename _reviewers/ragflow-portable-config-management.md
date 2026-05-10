---
title: Portable Config Management
description: 'When changing configuration, treat runtime configuration as the source
  of truth and avoid embedding/duplicating settings.


  Apply these rules:

  1) Prefer `.env` + `env_file: .env` and avoid duplicating the same variables in
  multiple places.'
repository: infiniflow/ragflow
label: Configurations
language: Yaml
comments_count: 5
repository_stars: 80174
---

When changing configuration, treat runtime configuration as the source of truth and avoid embedding/duplicating settings.

Apply these rules:
1) Prefer `.env` + `env_file: .env` and avoid duplicating the same variables in multiple places.
2) Do not hard-code environment-specific identifiers like `container_name` in shared compose files.
3) For frequently changed/overridden configuration (including templates), mount files via volumes rather than baking templates into images that would require rebuilds to take effect.
4) If one setting is coupled to another (e.g., application upload limits and nginx limits), update both together.

Example (compose):
```yaml
services:
  app:
    env_file: .env
    # no container_name in shared files
    volumes:
      - ./service_conf.yaml:/ragflow/conf/service_conf.yaml
```