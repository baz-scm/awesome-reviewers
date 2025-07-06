---
title: Support all target environments
description: When managing dependency configurations (Pipfiles, requirements.txt,
  lock files), ensure compatibility with all supported environments in your project.
  Package version requirements should work across all supported Python versions and
  deployment environments.
repository: bridgecrewio/checkov
label: Configurations
language: Other
comments_count: 3
repository_stars: 7667
---

When managing dependency configurations (Pipfiles, requirements.txt, lock files), ensure compatibility with all supported environments in your project. Package version requirements should work across all supported Python versions and deployment environments.

Adding version constraints in dependency configurations:
1. Verify compatibility with all supported Python versions
2. Test configurations in all CI environments before committing
3. If version locking is necessary, document the reason as a comment
4. Consider separate PRs for dependency updates that require code changes

Example:
```
# Bad practice - locks to specific version that may not support all environments
asteval = "==1.0.6"  # Only supports Python 3.10+

# Good practice - explicitly specify a compatible version range
asteval = ">=0.9.27,<1.1.0"  # Supports Python 3.8 and above

# If version locking is necessary, include a comment explaining why
mypy = "==1.13.0"  # Locked temporarily to avoid breaking changes, see PR #1234 for update plan
```