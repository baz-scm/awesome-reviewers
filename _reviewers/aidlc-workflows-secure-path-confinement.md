---
title: Secure Path Confinement
description: 'Enforce security boundaries using robust validation and least-privilege
  isolation.


  - For filesystem access restricted to a base directory (e.g., a “run folder”), never
  use string prefix checks like `str(path).startswith(...)` to prevent `../` traversal
  or sibling-dir prefix bypasses. Instead, use `Path.is_relative_to`.'
repository: awslabs/aidlc-workflows
label: Security
language: Python
comments_count: 3
repository_stars: 3849
---

Enforce security boundaries using robust validation and least-privilege isolation.

- For filesystem access restricted to a base directory (e.g., a “run folder”), never use string prefix checks like `str(path).startswith(...)` to prevent `../` traversal or sibling-dir prefix bypasses. Instead, use `Path.is_relative_to`.
- For untrusted command execution, treat the sandbox as part of your security model: run with resource limits, drop capabilities, avoid root via `--user=os.getuid():os.getgid()`, and scrub credentials from both stdout/stderr before returning/logging.

Example (path confinement):
```python
from pathlib import Path

def resolve_safe(run_folder: Path, relative_path: str) -> Path:
    resolved = (run_folder / relative_path).resolve()
    run_resolved = run_folder.resolve()
    if not resolved.is_relative_to(run_resolved):
        raise ValueError("Path escapes run folder")
    return resolved
```

Example (sandbox hardening pattern):
```python
import os, subprocess
from shared.credential_scrubber import scrub_credentials

result = subprocess.run(
    [
        "docker", "run", "--rm",
        "--cap-drop=ALL",
        f"--user={os.getuid()}:{os.getgid()}",
        "--memory=2g", "--cpus=2",
        "-v", f"{workspace.resolve()}:/workspace",
        "image", "bash", "-c", command,
    ],
    capture_output=True, text=True, timeout=timeout,
)
stdout = scrub_credentials(result.stdout)
stderr = scrub_credentials(result.stderr)
```