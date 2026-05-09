---
title: Include API Version
description: When configuring client access to an external API, store the provider’s
  base endpoint as a fully-qualified URL that already includes the required API version
  (and defaults). Avoid splitting “base URL” and “version” in ways that can drift
  or be forgotten—make the endpoint unambiguous.
repository: coleam00/Archon
label: API
language: Other
comments_count: 2
repository_stars: 21089
---

When configuring client access to an external API, store the provider’s base endpoint as a fully-qualified URL that already includes the required API version (and defaults). Avoid splitting “base URL” and “version” in ways that can drift or be forgotten—make the endpoint unambiguous.

Example (.env.example style):
```bash
# Provider base endpoint including version path
OPENAI_ENDPOINT=https://api.openai.com/v1

# If using Azure, include the full endpoint and keep the version as part of the endpoint you call
# (or ensure the final request URL includes the version parameter/path consistently)
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_API_VERSION=2024-xx-xx
```

Application guidance:
- Document the expected value format for `*_ENDPOINT` (include `/v1` or the API-version component).
- Provide a default when the env var is absent (e.g., default to `https://api.openai.com/v1`).
- Ensure request construction uses the configured endpoint directly (so the effective request URL always contains the correct API version).