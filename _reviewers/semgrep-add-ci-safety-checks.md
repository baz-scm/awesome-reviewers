---
title: Add CI safety checks
description: Implement defensive checks and error handling in CI/CD workflows to prevent
  failures and ensure robust operations. This includes validating preconditions, checking
  for edge cases, and using appropriate tools that preserve important information.
repository: semgrep/semgrep
label: CI/CD
language: Other
comments_count: 4
repository_stars: 12598
---

Implement defensive checks and error handling in CI/CD workflows to prevent failures and ensure robust operations. This includes validating preconditions, checking for edge cases, and using appropriate tools that preserve important information.

Key practices:
- Add validation checks before critical operations to prevent duplicate or conflicting actions
- Use proper tools that preserve metadata (e.g., `git am` instead of `patch` to maintain author information)
- Verify platform compatibility when adding new dependencies
- Implement comprehensive testing that covers all supported environments

Example from sync workflow:
```bash
# Check if commit already synced to prevent duplicates
if git show --stat HEAD | grep -q "synced from"; then
    echo "error: HEAD commit already comes from Pro and cannot be synced"
    exit 1
fi

# Use git am to preserve author info instead of patch
sed -E 's:( a| b)/:\1OSS/:g' 0001-*.patch >pro.patch
git am pro.patch
```

This approach prevents common CI failures, reduces debugging time, and ensures workflows handle edge cases gracefully while maintaining data integrity.