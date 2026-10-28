---
title: Revalidate artifacts at each stage
description: When performing security-relevant validation on build artifacts (e.g.,
  verifying a binary uses the expected static runtime, checking signatures, or confirming
  integrity), do not assume a check performed at an early stage still holds later
  in the pipeline. Artifacts can be swapped, rebuilt, or tampered with between staging
  and packaging/archiving, so re-run...
repository: ogulcancelik/herdr#canary966c66ad
label: Security
language: Python
comments_count: 1
repository_stars: 46332
---

When performing security-relevant validation on build artifacts (e.g., verifying a binary uses the expected static runtime, checking signatures, or confirming integrity), do not assume a check performed at an early stage still holds later in the pipeline. Artifacts can be swapped, rebuilt, or tampered with between staging and packaging/archiving, so re-run the validation immediately before the artifact is consumed or shipped (e.g., re-validate right before `archive_bundle` packages the staged files), in addition to any earlier checks. Add tests that simulate tampering after each stage (e.g., swap `herdr.exe` for a dynamically-linked build after staging) to confirm the revalidation actually rejects bad artifacts.

Example pattern:
```python
def stage_bundle(...):
    validate_static_msvc_runtime(herdr_exe.read_bytes(), herdr_exe.name)
    # ... copy herdr_exe into stage ...

def validate_stage(stage_dir):
    staged_exe = stage_dir / "herdr.exe"
    validate_static_msvc_runtime(staged_exe.read_bytes(), staged_exe.name)

def archive_bundle(stage_dir, ...):
    validate_stage(stage_dir)  # re-check before packaging, even if staging already validated
    ...
```
This closes the gap between validation and use, preventing a validated check from being bypassed by a later substitution of the artifact.</description>
</invoke>
