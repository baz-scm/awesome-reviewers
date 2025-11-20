---
title: CI blocking with overrides
description: When implementing CI checks that can block pull request merges, always
  provide clear override mechanisms for exceptional cases. Hard-failing CI checks
  should be strong signals to developers, but teams need escape hatches when legitimate
  exceptions arise.
repository: strands-agents/sdk-python
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 4044
---

When implementing CI checks that can block pull request merges, always provide clear override mechanisms for exceptional cases. Hard-failing CI checks should be strong signals to developers, but teams need escape hatches when legitimate exceptions arise.

Design your CI workflows to fail meaningfully while maintaining flexibility:

```yaml
# Example: PR size check with override capability
- name: Check PR size
  run: |
    if [ $TOTAL_CHANGES -gt 1000 ]; then
      echo "PR is too large ($TOTAL_CHANGES lines). Please split into smaller PRs."
      echo "To override, add 'override-size-check' label and provide justification."
      exit 1
    fi
```

Key considerations:
- Use hard failures for important quality gates (like PR size limits) rather than just warnings
- Document override procedures clearly (labels, manual approval, etc.)
- Expect CI rules to evolve as teams learn what thresholds work best
- Ensure overrides require justification to maintain accountability

This approach provides strong developer guidance while acknowledging that exceptional cases requiring large PRs will occasionally arise and need a path forward.