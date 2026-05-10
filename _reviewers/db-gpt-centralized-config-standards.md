---
title: Centralized Config Standards
description: When implementing new behavior behind feature flags or configuration
  (paths, env vars, index dimensions, toggles like text2gql), use centralized, documented
  config instead of hardcoded values or scattered env access.
repository: eosphoros-ai/DB-GPT
label: Configurations
language: Python
comments_count: 13
repository_stars: 18703
---

When implementing new behavior behind feature flags or configuration (paths, env vars, index dimensions, toggles like text2gql), use centralized, documented config instead of hardcoded values or scattered env access.

Apply these rules:
1) No absolute paths/constants in code: resolve paths from config/env (with sensible defaults).
2) Use feature flags from config and keep them consistent across code/docs/.env.template.
3) Avoid “parameter explosion”: encapsulate related settings into a dedicated *Config object and pass that object (or access via get_config()) instead of threading many constructor args.
4) Don’t read os.getenv in feature logic; normalize env->config during config building.
5) Don’t hardcode tunables (e.g., embedding/index dimension); pull them from config.
6) Keep layer boundaries: app-layer settings (e.g., CFG/proxy/app-specific knobs) should be passed down as explicit parameters/config, not embedded in lower modules.

Example (replace absolute paths with config):
```python
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataManusConfig:
    db_path: str
    excel_path: str

def load_config() -> DataManusConfig:
    # normalize env in one place (not throughout business logic)
    import os
    return DataManusConfig(
        db_path=os.getenv("DATA_MANUS_DB_PATH", "./examples/test_files/datamanus_test.db"),
        excel_path=os.getenv("DATA_MANUS_EXCEL_PATH", "./examples/test_files/employer_info.xlsx"),
    )

def build_connector(cfg: DataManusConfig):
    db_file = Path(cfg.db_path).expanduser().resolve()
    return SQLiteConnector.from_file_path(str(db_file))
```

Checklist for each PR:
- [ ] Are any file system paths or magic numbers hardcoded? Replace with config.
- [ ] Is any new env var/flag added with a default and included in .env.template + docs?
- [ ] Does the new code read env directly instead of going through config normalization?
- [ ] Are constructors receiving many unrelated parameters instead of a single encapsulated config?