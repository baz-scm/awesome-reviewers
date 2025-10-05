---
title: Pin dependency versions
description: Always pin specific versions of dependencies, tools, and commits in configuration
  files to ensure consistent behavior across environments and deployments. When pinning
  versions, include comments explaining the reasoning behind the specific version
  choice.
repository: commaai/openpilot
label: Configurations
language: Shell
comments_count: 3
repository_stars: 58214
---

Always pin specific versions of dependencies, tools, and commits in configuration files to ensure consistent behavior across environments and deployments. When pinning versions, include comments explaining the reasoning behind the specific version choice.

This practice prevents unexpected breakages from automatic updates and ensures all team members and deployment environments use identical dependency versions. When allowing version overrides through parameters, maintain the pinned version as the default fallback.

Example:
```bash
# Pin specific versions with explanatory comments
brew "llvm@19"  # pinned for tinygrad compatibility

# In build scripts, allow override but keep pinned default
COMMIT="${1:-66030a7de62c9e1ee8ab30a1d657a740333bb4f2}"  # default pinned commit

# Version numbers should be incremented properly
export AGNOS_VERSION="12"  # increment ensures all devices run same version
```

This approach maintains stability while allowing flexibility when needed, and the comments help future maintainers understand the rationale behind version choices.