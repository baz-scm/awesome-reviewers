---
title: Explicit over implicit
description: 'Always prefer explicit configuration settings over relying on implicit
  defaults or environmental behaviors in CI workflows and build configurations. This
  is particularly important for:'
repository: pydantic/pydantic
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 24377
---

Always prefer explicit configuration settings over relying on implicit defaults or environmental behaviors in CI workflows and build configurations. This is particularly important for:

1. **Python version specifications**: Always explicitly specify the Python version in commands even when tools might detect it automatically.

```yaml
# Good - explicitly specifies Python version
- name: Set up Python 3.12
  run: uv python install 3.12

- name: Install dependencies
  run: uv sync --python 3.12 --group docs
```

2. **Dependency extras and groups**: Clearly state which extras and dependency groups are being included in installation commands.

```yaml
# Good - explicitly states which extras are being installed
- name: Install dependencies
  run: uv sync --extra timezone

# Good - step name clearly indicates what's being tested
- name: Test without email-validator
  run: ...
```

This approach prevents unexpected behaviors from implicit configurations (like .python-version files) and makes workflows more maintainable and predictable, especially in CI environments where consistency is critical.