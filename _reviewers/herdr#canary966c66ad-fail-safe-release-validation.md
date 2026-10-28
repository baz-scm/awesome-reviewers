---
title: Fail-safe release validation
description: Release and packaging scripts must treat any unexpected or out-of-contract
  state as a hard, explicit failure rather than attempting silent or automatic recovery
  (e.g., no automatic backup/restore/overwrite of installed bundles when contents
  differ — stop and require manual intervention instead). Validation logic in these
  scripts should be strict and robust:...
repository: ogulcancelik/herdr#canary966c66ad
label: CI/CD
language: Python
comments_count: 3
repository_stars: 46332
---

Release and packaging scripts must treat any unexpected or out-of-contract state as a hard, explicit failure rather than attempting silent or automatic recovery (e.g., no automatic backup/restore/overwrite of installed bundles when contents differ — stop and require manual intervention instead). Validation logic in these scripts should be strict and robust: use allowlists for what is permitted to change (e.g., only specific release files, or only a version bump in Cargo.toml/Cargo.lock), reject disallowed substitutions such as regular files becoming symlinks or submodules, and detect problematic artifacts by matching families/prefixes (e.g., `vcruntime140`, `msvcp140`, `ucrtbase`) rather than enumerating exact filenames, since enumeration misses variants like debug builds (`MSVCP140D.dll`, `ucrtbased.dll`). Every such fix should come with a regression test covering the edge case that was missed, so future changes can't silently reintroduce the gap. For example, prefer:

```python
if not matches:
    raise ValueError("installed bundle differs from staged bundle; remove it and re-run")
```

over automatically deleting backups and overwriting installed files, and prefer prefix-based detection:

```python
DYNAMIC_MSVC_RUNTIME_PREFIXES = ("vcruntime140", "msvcp140", "concrt140", "ucrtbase", "api-ms-win-crt-")
```

over a fixed list of exact filenames.</description>
