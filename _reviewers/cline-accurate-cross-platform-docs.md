---
title: Accurate, Cross-Platform Docs
description: When updating technical documentation, ensure it is operationally accurate
  across supported platforms and matches the actual behavior of the software.
repository: CLINE/CLINE
label: Documentation
language: Other
comments_count: 2
repository_stars: 70837
---

When updating technical documentation, ensure it is operationally accurate across supported platforms and matches the actual behavior of the software.

Apply this standard:
- **Verify path/environment semantics by OS**: If docs mention `~`, home directories, or filesystem paths, confirm how that expands on each supported OS (e.g., Windows user/profile vs roaming profile behavior). If ambiguity exists, document the concrete path(s) or provide OS-specific examples.
- **Keep CLI/API docs behavior-faithful**: Generate/confirm option lists and examples from the real implementation (`--help`, command parsing, and tests). Don’t include flags/options that are “accepted but ignored”; remove or correct them.
- **Match detailed behavior**: If defaults or ordering differ (e.g., paging/limits returning newest-first), reflect that precisely in the docs.

Example (behavior-faithful option table + example):
```bash
# Doc should only list options that actually work
cline history --json --limit 10

# If an option was removed or ignored, update the docs accordingly
# (e.g., remove the option row rather than saying it’s ignored)
```