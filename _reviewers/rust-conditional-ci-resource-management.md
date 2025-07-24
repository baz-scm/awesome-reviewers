---
title: Conditional CI resource management
description: Configure CI workflows to intelligently manage system resources through
  conditional execution rather than duplicating steps. Use matrix variables or job
  conditions to determine when resource-intensive operations should run.
repository: rust-lang/rust
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 105254
---

Configure CI workflows to intelligently manage system resources through conditional execution rather than duplicating steps. Use matrix variables or job conditions to determine when resource-intensive operations should run.

For resource monitoring tasks (like disk usage checks), define a condition that prevents redundant execution:

```yaml
- name: print disk usage
  # Only run this step if the free_disk operation isn't executed
  if: ${{ !matrix.free_disk }}
  run: |
    echo "disk usage:"
    df -h
```

When configuring runners, explicitly document resource constraints and set appropriate flags that control resource management steps:

```yaml
runners:
  - &job-windows
    os: windows-2025
    free_disk: true  # Explicitly mark jobs that need disk space freed
    <<: *base-job
```

This approach keeps workflows maintainable by avoiding duplicative steps, makes resource constraints visible, and ensures consistent behavior across different execution environments.