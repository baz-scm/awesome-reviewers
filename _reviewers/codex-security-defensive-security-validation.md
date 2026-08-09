---
title: Defensive Security Validation
description: 'Apply defensive validation rules anywhere code derives security decisions
  from paths, filesystem objects, executables, or integrity metadata.


  Guidelines'
repository: openai/codex-security
label: Security
language: Python
comments_count: 5
repository_stars: 9394
---

Apply defensive validation rules anywhere code derives security decisions from paths, filesystem objects, executables, or integrity metadata.

Guidelines
1) Path inclusion/exclusion must be precise
- Don’t blanket-exclude “global” directories if that can filter out security-relevant first-party files.
- Prefer positive inclusion for known security-relevant filenames/directories, then apply narrow exclusions.

2) Treat special filesystem objects as unsafe
- Symlinks: assume they can escape the intended repository boundary.
- Pipes/FIFOs: assume they may hang during reads.
- Action: reject or defer these paths (e.g., force mandatory full handling) rather than producing empty/benign previews.

3) Executable boundary + identity safety
- If selecting an external command (e.g., git), validate the canonical target and ensure it stays within the expected boundary.
- Invoke the original absolute path you intended to run; avoid executing a different canonical target that changes identity/argv behavior.

4) Enforce integrity on security-critical transitions
- Require exact digest matches for current selections.
- Legacy/compatibility acceptance must be explicitly versioned and cannot silently “drift” after staged changes.

5) Never reinterpret security-critical metadata unless fully supported
- When adopting a registered “kind” or similar label, only allow it if the trusted binding provides (or overwrites) all kind-dependent coordinate fields required for correctness.

Example pattern (illustrative)
```python
from pathlib import Path

def safe_diff_path_allowed(repo: Path, rel: Path, status: str) -> bool:
    # 1) include security-relevant paths; narrow exclusions
    if rel.parts and rel.parts[0] == ".github":
        # allow security relevant subsets; avoid over-broad excludes
        pass

    # 2) reject unsafe filesystem object types (symlink/pipe)
    abs_path = repo / rel
    try:
        if abs_path.is_symlink() or abs_path.exists() and abs_path.is_fifo():
            return False  # force reject/defer to full review path
    except OSError:
        return False

    return status in {"M", "A", "C", "R" , "D" , "U"}  # as appropriate

# 4) integrity: exact digest required for current selections
def accept_selection(current_digest: str, selected_digest: str) -> bool:
    return current_digest == selected_digest

# 5) safe kind adoption: only if binding covers required coordinates
TARGET_REQUIRED_COORDINATE_FIELDS = {
    "git_revision": {"baseRevision","headRevision"},
    "git_worktree": {"requiredSnapshotDigest"},
    "git_diff": {"snapshotDigest"},
}

def maybe_adopt_kind(target: dict, allowed_kinds: list, binding: dict) -> None:
    if len(allowed_kinds) != 1:
        return
    registered_kind = allowed_kinds[0]
    if not isinstance(registered_kind, str):
        return
    if target.get("kind") == registered_kind:
        return
    required = TARGET_REQUIRED_COORDINATE_FIELDS.get(registered_kind, set())
    if not required <= binding.keys():
        return  # refuse reinterpretation
    target["kind"] = registered_kind
```

This prevents (a) security-relevant changes being filtered out, (b) unsafe reads/execution due to symlinks/pipes/shims, and (c) integrity breaks where security-critical metadata is silently reinterpreted or digests drift.