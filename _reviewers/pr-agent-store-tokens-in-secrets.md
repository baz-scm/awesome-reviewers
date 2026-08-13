---
title: Store Tokens in Secrets
description: Do not commit authentication credentials (e.g., GitHub personal access
  tokens, API keys, passwords) in versioned configuration files. Keep them in a dedicated
  secrets source such as `.secrets.toml` (or your secret manager), and ensure the
  committed config only contains placeholders/defaults.
repository: the-pr-agent/pr-agent
label: Security
language: Toml
comments_count: 1
repository_stars: 12523
---

Do not commit authentication credentials (e.g., GitHub personal access tokens, API keys, passwords) in versioned configuration files. Keep them in a dedicated secrets source such as `.secrets.toml` (or your secret manager), and ensure the committed config only contains placeholders/defaults.

Example (structure):
```toml
# configuration.toml (tracked)
[github]
deployment_type = "user"
user_token = "" # placeholder only
```
```toml
# .secrets.toml (not tracked / secured)
[github]
user_token = "ghp_..." # real PAT with minimal required scopes
```

Apply this by: (1) moving any `*_token`, `api_key`, `password`, or similar secret values to `.secrets.toml`; (2) adding/using ignore rules so secrets files are not committed; and (3) rotating any token that was accidentally checked in.