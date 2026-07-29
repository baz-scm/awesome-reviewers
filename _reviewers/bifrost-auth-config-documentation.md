---
title: Auth config documentation
description: 'When Helm (or other config) controls authentication for a protected
  endpoint, treat credential source, key names, and auth enablement paths as security-sensitive
  behavior. Ensure both the implementation and the accompanying docs/changelog precisely
  describe:'
repository: maximhq/bifrost
label: Security
language: Other
comments_count: 1
repository_stars: 6862
---

When Helm (or other config) controls authentication for a protected endpoint, treat credential source, key names, and auth enablement paths as security-sensitive behavior. Ensure both the implementation and the accompanying docs/changelog precisely describe:

- **Auth enablement outcome**: what happens to unauthenticated requests (e.g., `401` leading to Prometheus `up=0`).
- **Credential inheritance vs explicit override**:
  - Default behavior should state whether credentials and **their key names** are inherited from an auth configuration.
  - Any `existingSecret`/override should state that it **fully overrides** inherited secret identity and key mapping (i.e., keys come from the override’s `usernameKey`/`passwordKey`, not from the auth config’s key names).
- **Validation step**: verify documentation claims by inspecting the *rendered output* (e.g., via `helm template`) and confirming the exact Secret names and key fields.

Example validation approach:
```bash
helm template rel . \
  --set serviceMonitor.enabled=true \
  --set serviceMonitor.basicAuth.enabled=true \
  --set serviceMonitor.basicAuth.existingSecret=scrape-creds \
  --set bifrost.authConfig.existingSecret=bifrost-secrets \
  --set bifrost.authConfig.usernameKey=admin-username \
  --set bifrost.authConfig.passwordKey=admin-password

# Confirm rendered basicAuth uses scrape-creds with key names
# (e.g., username/password), not inherited admin-username/admin-password.
```

This prevents misleading security documentation that can cause operators to scrape with wrong credentials, misunderstand failure modes, or break credential rotation assumptions.