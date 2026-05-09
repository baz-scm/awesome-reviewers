---
title: Use authenticated env tokens
description: Any service exposed to the network (e.g., via Docker `ports`) must be
  protected with authentication, and any secret used for that auth (e.g., Jupyter
  token/password) must come from environment variables (e.g., `.env`) rather than
  being hardcoded in versioned files. If a compose file uses placeholder defaults,
  treat them as non-production scaffolding and...
repository: TauricResearch/TradingAgents
label: Security
language: Yaml
comments_count: 1
repository_stars: 71953
---

Any service exposed to the network (e.g., via Docker `ports`) must be protected with authentication, and any secret used for that auth (e.g., Jupyter token/password) must come from environment variables (e.g., `.env`) rather than being hardcoded in versioned files. If a compose file uses placeholder defaults, treat them as non-production scaffolding and require production overrides.

Example (secure pattern):
```yaml
services:
  jupyter:
    ports:
      - "8888:8888"
    env_file:
      - .env
    environment:
      # Put the real token in .env (do not commit it)
      - JUPYTER_TOKEN
    command: >-
      jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
      --ServerApp.token='${JUPYTER_TOKEN}'
```
Checklist:
- Store tokens/secrets only in `.env` (or a secret manager), not in the compose file.
- Ensure placeholders (e.g., `changeme`) are clearly non-production and never deployed as-is.
- Add/keep comments describing how to generate and set the secret so future hardening is straightforward.