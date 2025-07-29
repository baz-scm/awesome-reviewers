---
title: maintain security constraints
description: Always preserve existing security constraints and validation mechanisms
  rather than weakening them for convenience or functionality. When modifying authentication,
  validation, or security-related code, ensure that the changes maintain or strengthen
  the security posture.
repository: python-poetry/poetry
label: Security
language: Python
comments_count: 3
repository_stars: 33496
---

Always preserve existing security constraints and validation mechanisms rather than weakening them for convenience or functionality. When modifying authentication, validation, or security-related code, ensure that the changes maintain or strengthen the security posture.

Key principles:
- Don't bypass or weaken hash validation even when it seems unnecessary
- Maintain strict authentication precedence to prevent credential confusion
- Preserve security checks that prevent unauthorized access or data integrity issues

Example from hash validation:
```python
# Good: Maintain strict validation
known_hashes = {f["hash"] for f in package.files if f["file"] == archive.name}
if known_hashes and archive_hash not in known_hashes:
    # Still fails for security when no known hashes exist

# Bad: Weakening the constraint
if archive_hash not in known_hashes:  # Passes when known_hashes is empty
```

When in doubt about whether a security constraint is necessary, err on the side of maintaining it unless there's clear evidence it's safe to remove.