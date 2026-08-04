---
title: Config source alignment
description: When using configuration via `.env`/config files, make the notebook’s
  behavior match what the docs and environment files claim—and ensure fresh environments
  can run the notebook reliably.
repository: awslabs/agentcore-samples
label: Configurations
language: Other
comments_count: 4
repository_stars: 3244
---

When using configuration via `.env`/config files, make the notebook’s behavior match what the docs and environment files claim—and ensure fresh environments can run the notebook reliably.

Apply these standards:
1) **Feature flags/config precedence must be documented correctly**
- If code loads flags from `.env` (e.g., reloads via `load_dotenv(override=True)`), your markdown must say to set the flag in `.env`, not as an inline variable.
- Ensure the flag name in docs exactly matches the code (e.g., `RUN_LIVE_RUNTIME` vs `RUN_LIVE`).

2) **Keep `.env.example` credential-safe and consistent with tooling**
- Don’t include sample static AWS access keys as the recommended path.
- Prefer documenting `aws configure` or environment-variable/instance-role based credential providers.

3) **Make imports portable across environments**
- Avoid fragile relative imports that depend on the current working directory.
- If you need local-module imports, set `sys.path` based on the notebook/script location.

Example (portable import setup):
```python
import os
import sys

current_dir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(current_dir)

from custom_memory_prompts import consolidation_prompt, extraction_prompt
```

4) **Ship explicit dependencies and install steps**
- Use a `requirements.txt` for notebook dependencies and add Jupyter-friendly install instructions.
- Remove unused imports (e.g., `import yaml` if not used) to reduce confusion about required packages.

Outcome: configuration-driven execution is predictable (flags/precedence are correct), secure (credentials aren’t mishandled), and reproducible (imports/dependencies work on a clean setup).