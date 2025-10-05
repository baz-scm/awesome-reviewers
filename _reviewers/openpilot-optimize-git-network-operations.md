---
title: Optimize git network operations
description: When performing git operations that involve network communication, use
  proper syntax and efficient strategies to minimize data transfer and ensure correct
  remote branch handling.
repository: commaai/openpilot
label: Networking
language: Shell
comments_count: 2
repository_stars: 58214
---

When performing git operations that involve network communication, use proper syntax and efficient strategies to minimize data transfer and ensure correct remote branch handling.

For remote branch fetching, always specify both remote and local branch names to avoid ambiguity and ensure the branch is properly tracked locally:

```bash
# Preferred: explicit remote:local syntax
git fetch origin $1:$1

# Avoid: ambiguous fetch that may not create local branch
git fetch origin $1
```

For repository cloning, consider using shallow clones with `--depth=1` to reduce initial network transfer, especially for testing or CI environments where full history isn't needed:

```bash
# Efficient for testing/CI
git clone --depth=1 https://github.com/user/repo.git

# Note: shallow clones can be unshallowed later if needed
git fetch --unshallow
```

This approach reduces network bandwidth usage while maintaining the ability to expand the repository scope when necessary. Always consider the trade-offs between initial clone speed and future git operation capabilities when choosing clone strategies.