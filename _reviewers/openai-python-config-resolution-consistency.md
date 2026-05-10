---
title: Config resolution consistency
description: 'When adding or extending client/provider integrations, enforce a single,
  predictable configuration-resolution contract:


  - **Args → env fallbacks:** For each required setting (e.g., `api_version`, `region`),
  accept an explicit argument, otherwise fall back to the corresponding environment
  variable(s). Only raise a clear error when *neither* is provided.'
repository: openai/openai-python
label: Configurations
language: Python
comments_count: 4
repository_stars: 30731
---

When adding or extending client/provider integrations, enforce a single, predictable configuration-resolution contract:

- **Args → env fallbacks:** For each required setting (e.g., `api_version`, `region`), accept an explicit argument, otherwise fall back to the corresponding environment variable(s). Only raise a clear error when *neither* is provided.
- **Keep derived config coherent on overrides:** If your client derives other settings from config (e.g., `base_url` derived from `region`), then `copy()`/cloning/overrides must recompute or correctly forward dependent values so behavior matches the updated config.
- **Prevent invalid config-mode switches:** If auth modes are mutually exclusive (e.g., SigV4 vs API key, or token vs API key), ensure `copy()` clears/normalizes incompatible fields instead of forwarding stale state.
- **Stability across releases & feature flags:**
  - If an integration requires adding public exports (like `__init__.py`), update the generator configuration so the change persists across automated releases.
  - Manage optional feature dependencies (e.g., async HTTP support) via extras/feature flags and raise a focused runtime error when the optional dependency isn’t installed.

Example patterns:

```python
# 1) Env fallback + clear error
resolved_api_version = api_version or os.environ.get("OPENAI_API_VERSION")
if not resolved_api_version:
    raise ValueError("Must provide api_version or set OPENAI_API_VERSION")

# 2) copy(): keep dependent config consistent
new_region = region or self._region
# ensure base_url is recalculated when region changes
_forward_base_url = {} if region else {"base_url": self.base_url}

# 3) copy(): normalize mutually-exclusive auth fields
# if switching to api_key, drop credential provider
forwarded_credential_provider = None if "api_key" in kwargs else (credential_provider or self._credential_provider)
```

Add unit tests that cover:
- override of primary config triggers correct recomputation of dependent config (e.g., `region` → `base_url`),
- explicit switches between mutually exclusive auth modes behave as expected,
- missing required config produces the intended error message and does not fail later with confusing downstream exceptions.