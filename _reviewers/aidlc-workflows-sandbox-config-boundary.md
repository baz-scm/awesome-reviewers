---
title: Sandbox config boundary
description: 'When a feature flag like `use_sandbox` changes where code runs (host
  vs container), treat it as a configuration boundary: (1) explicitly provide the
  container environment your tools expect, and (2) remove/recreate any stateful artifacts
  created on the other side.'
repository: awslabs/aidlc-workflows
label: Configurations
language: Python
comments_count: 3
repository_stars: 3849
---

When a feature flag like `use_sandbox` changes where code runs (host vs container), treat it as a configuration boundary: (1) explicitly provide the container environment your tools expect, and (2) remove/recreate any stateful artifacts created on the other side.

Practical rules:
- Always set container `HOME` (and cache dirs) explicitly when running as a mapped/non-root UID so tools can write caches:
  - `HOME=/tmp`
  - `UV_CACHE_DIR=/tmp/.cache/uv`
  - `NPM_CONFIG_CACHE=/tmp/.cache/npm`
- If sandboxing is enabled, delete host-created `.venv` (or any venv-like directory) before running installs/tests inside the container, then recreate it in the sandbox to avoid broken symlinks to host interpreters.

Example (pattern):
```python
def prepare_for_sandbox(project_root: Path, use_sandbox: bool) -> None:
    if use_sandbox:
        stale_venv = project_root / ".venv"
        if stale_venv.is_dir():
            shutil.rmtree(stale_venv)


env = {
    "HOME": "/tmp",
    "UV_CACHE_DIR": "/tmp/.cache/uv",
    "NPM_CONFIG_CACHE": "/tmp/.cache/npm",
}

sandbox_run(
    command=..., 
    workspace=..., 
    network=True,
    env=env,
    # ... other sandbox config ...
)
```