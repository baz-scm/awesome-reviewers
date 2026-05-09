---
title: Configuration Source of Truth
description: 'Maintain configuration in a single, consistent way across the codebase:


  - **Use explicit defaults + safe fallbacks:** If function parameters accept `None`,
  resolve them via config defaults (and document why). Prefer provider-specific keys
  so changing one provider doesn’t silently alter another.'
repository: TauricResearch/TradingAgents
label: Configurations
language: Python
comments_count: 3
repository_stars: 71953
---

Maintain configuration in a single, consistent way across the codebase:

- **Use explicit defaults + safe fallbacks:** If function parameters accept `None`, resolve them via config defaults (and document why). Prefer provider-specific keys so changing one provider doesn’t silently alter another.
- **Avoid duplicated “source of truth”:** If base URLs / endpoints / constants are repeated across modules, centralize them (e.g., one dict/module imported everywhere) rather than copying per file.
- **Stay aligned with shared validation:** When configs are meant to represent “valid” values (e.g., model names), mirror the upstream/default config + validators. If you need to change allowed values, do it via the upstream/shared change—not by diverging locally.

Example pattern (provider-specific defaults + None fallback):

```py
def get_global_news(curr_date, look_back_days: int | None = 7, limit: int | None = 50) -> dict:
    # Resolve None via provider-specific config keys
    if look_back_days is None:
        look_back_days = DEFAULT_CONFIG.get("global_news_look_back_days", 7)
    if limit is None:
        # Keep Alpha Vantage historical default separate from other providers
        limit = DEFAULT_CONFIG.get("av_global_news_limit", 50)
    ...
```

Follow-up actions when issues are found:
- If you add a new provider, **update the centralized config mapping** once (and remove/avoid duplicating URLs elsewhere).
- If you adjust valid model/provider values, **open an upstream-wide PR** so validators/defaults stay consistent.