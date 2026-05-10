---
title: Safe configuration changes
description: 'When updating configuration/env logic, treat it as compatibility-sensitive:
  preserve existing default behavior and env var formats, avoid enabling config blocks
  that silently change runtime semantics, and ensure config typing and dependent settings
  stay consistent.'
repository: infiniflow/ragflow
label: Configurations
language: Other
comments_count: 5
repository_stars: 80174
---

When updating configuration/env logic, treat it as compatibility-sensitive: preserve existing default behavior and env var formats, avoid enabling config blocks that silently change runtime semantics, and ensure config typing and dependent settings stay consistent.

Apply these rules:
- Preserve existing env var formats/semantics (or add a compatibility path). Example: keep ES_HOST in its prior format rather than switching it to a URL if templates still assume the old form.
- Don’t uncomment/enable template sections that change defaults. Prefer explicit flags controlled via the corresponding .env.
- Keep .env and config templates in sync; if versions can diverge for users, make the smallest possible change to reduce confusion/breakage.
- Ensure correct config types: in YAML templates, don’t accidentally turn numbers into strings (e.g., quoting values can cause type errors).
- Update paired dependent configs when you change limits/settings (e.g., if you change MAX_CONTENT_LENGTH, also update nginx client_max_body_size).

Example pattern (YAML typing):
```yaml
# Good: numeric port
port: '${MYSQL_PORT:-3306}'

# Avoid patterns that can cause type issues depending on templating/YAML parsing rules
# e.g., port: '3306' (string) if the consumer expects an int
```