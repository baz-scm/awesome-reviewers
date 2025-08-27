---
title: Automate sensitive CI artifacts
description: Large files and security-sensitive artifacts should be automatically
  generated in CI/CD pipelines rather than manually committed to version control.
  This reduces security risks from potentially malicious content and ensures artifacts
  stay current with the codebase.
repository: bazelbuild/bazel
label: CI/CD
language: Other
comments_count: 2
repository_stars: 24489
---

Large files and security-sensitive artifacts should be automatically generated in CI/CD pipelines rather than manually committed to version control. This reduces security risks from potentially malicious content and ensures artifacts stay current with the codebase.

For large profile files or binary artifacts, implement automated generation through CI jobs or release pipelines:

```python
# Instead of committing large profile files directly
# Use CI to regenerate profiles automatically
def regenerate_profile():
    # Run profiling in controlled CI environment
    bazel run //tools:profile_generator
    # Output profile as build artifact
```

Additionally, follow organizational policies for dependency placement. Files that could create bundling dependencies should be placed in appropriate directories (like `tools/` instead of `third_party/`) and explicitly documented:

```python
# Move sensitive configs to policy-compliant locations
# tools/proguard/config.proguard instead of third_party/
# Add to exclude lists to document the choice
exclude = ["tools/proguard/config.proguard"]
```

This approach ensures CI/CD security, maintains compliance with organizational policies, and keeps sensitive artifacts synchronized with code changes through automation.