---
title: Config source precedence
description: When configuration is moved/renamed or when settings are derived from
  environment variables, ensure (1) the dotenv loader points to the correct file path/name
  and (2) there is an explicit precedence order for derived settings (env-provided
  values override generated/default values).
repository: agent0ai/agent-zero
label: Configurations
language: Python
comments_count: 2
repository_stars: 17612
---

When configuration is moved/renamed or when settings are derived from environment variables, ensure (1) the dotenv loader points to the correct file path/name and (2) there is an explicit precedence order for derived settings (env-provided values override generated/default values).

Apply this as two concrete checks:
- **Config file correctness:** If you migrate `.env` (or stop using `default.env`), update the code that resolves the env file path (e.g., avoid loaders that still call something like `get_abs_path('.env')` when the new location is `usr/.env` or similar). Also remove references to env filenames you don’t actually use.
- **Precedence for derived settings:** For settings like tokens/keys, implement a deterministic rule: read the override from dotenv/env first; if missing/empty, fall back to `create_*` or other defaults.

Example pattern:
```py
import dotenv

def apply_settings(copy: dict) -> None:
    # precedence: env override > generated default
    external_key = dotenv.get_dotenv_value("A0_EXTERNAL_API_KEY")
    if external_key:
        copy["mcp_server_token"] = external_key
    else:
        copy["mcp_server_token"] = create_auth_token()
```
