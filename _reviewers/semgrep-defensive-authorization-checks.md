---
title: Defensive authorization checks
description: Always implement explicit authentication and authorization checks before
  granting access to premium features or sensitive operations, even when other conditions
  might imply proper authorization. Use defensive programming to prevent accidental
  privilege escalation.
repository: semgrep/semgrep
label: Security
language: Python
comments_count: 3
repository_stars: 12598
---

Always implement explicit authentication and authorization checks before granting access to premium features or sensitive operations, even when other conditions might imply proper authorization. Use defensive programming to prevent accidental privilege escalation.

This practice prevents security vulnerabilities where changes to one part of the system could inadvertently bypass authorization controls elsewhere. Always validate both the user's authentication state and their specific permissions for the requested operation.

Example implementation:
```python
# Bad: Relying on implicit authorization
if scan_handler and scan_handler.deepsemgrep:
    requested_engine = cls.PRO_INTERFILE

# Good: Explicit defensive checks
if scan_handler and scan_handler.deepsemgrep and logged_in:
    requested_engine = cls.PRO_INTERFILE
elif not logged_in and requested_engine != cls.OSS:
    raise SemgrepError("Premium features require authentication")
```

Key principles:
- Separate authentication concerns from feature logic
- Add explicit checks even when they seem redundant
- Fail securely when authorization is unclear
- Document security assumptions in comments