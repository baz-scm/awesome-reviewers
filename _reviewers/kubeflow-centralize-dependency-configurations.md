---
title: Centralize dependency configurations
description: When adding or updating package dependencies, place them in centralized
  configuration files rather than duplicating them across multiple services. Keep
  dependencies up-to-date with the latest stable versions and replace deprecated packages
  with their recommended successors. Always verify backward compatibility when upgrading
  dependency versions.
repository: kubeflow/kubeflow
label: Configurations
language: Txt
comments_count: 2
repository_stars: 15064
---

When adding or updating package dependencies, place them in centralized configuration files rather than duplicating them across multiple services. Keep dependencies up-to-date with the latest stable versions and replace deprecated packages with their recommended successors. Always verify backward compatibility when upgrading dependency versions.

Example for centralization:
```python
# Instead of:
# Adding to components/crud-web-apps/jupyter/backend/requirements.txt
# kubernetes==v22.6.0

# Do this:
# Update in components/crud-web-apps/common/backend/setup.py
install_requires=[
    "kubernetes>=22.6.0",
    # other dependencies
]
```

Example for replacing deprecated packages:
```
# Don't:
kfserving==0.5.1  # deprecated package

# Do:
kserve==0.11.1  # recommended successor
```
