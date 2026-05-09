---
title: Align Mount Paths
description: When configuring Docker bind mounts (or any persistence paths), set the
  container mount target to exactly where the application writes at runtime—especially
  when code uses relative paths like `Path.cwd() / "..."`. Don’t pick mount targets
  by convention; derive them from the actual path resolution logic.
repository: TauricResearch/TradingAgents
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 71953
---

When configuring Docker bind mounts (or any persistence paths), set the container mount target to exactly where the application writes at runtime—especially when code uses relative paths like `Path.cwd() / "..."`. Don’t pick mount targets by convention; derive them from the actual path resolution logic.

How to apply:
- In the code, find where files are written (e.g., `save_report_to_disk()`), and note the base path (often `Path.cwd()`).
- Determine the container working directory (`WORKDIR`) so `Path.cwd()` resolves to a specific absolute path in the container.
- Configure the bind mount so the host directory maps to that resolved absolute path.

Example:
```python
# writes to a path relative to the container working directory
out_path = Path.cwd() / "reports"
out_path.mkdir(parents=True, exist_ok=True)
``` 
```yaml
# bind the host reports dir to the container cwd-resolved reports dir
services:
  app:
    working_dir: /home/appuser/app
    volumes:
      - ./reports:/home/appuser/app/reports
``` 
This ensures user-facing generated artifacts persist to the intended host location, rather than accidentally redirecting only unrelated logs or internal files.