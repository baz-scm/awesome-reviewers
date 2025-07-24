---
title: precise security pattern matching
description: When checking for security features or configurations in shell scripts,
  use precise pattern matching to avoid false positives and limit information exposure.
  Instead of broad substring matches that could match unintended content, use specific
  patterns and restrict output to only necessary information.
repository: docker/compose
label: Security
language: Shell
comments_count: 1
repository_stars: 35858
---

When checking for security features or configurations in shell scripts, use precise pattern matching to avoid false positives and limit information exposure. Instead of broad substring matches that could match unintended content, use specific patterns and restrict output to only necessary information.

For example, when checking for Docker's user namespace security feature:

```bash
# Avoid: broad matching that could have false positives
if [ ! -z "$(docker info 2>/dev/null | grep userns)" ]; then

# Better: precise matching with limited output
if docker info --format '{{json .SecurityOptions}}' 2>/dev/null | grep -q 'name=userns'; then
```

This approach reduces the risk of incorrectly identifying security features and minimizes information leakage by querying only the specific data needed for the security check.