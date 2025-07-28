---
title: Validate CI/CD timing checks
description: When implementing timing-based security checks in CI/CD workflows, ensure
  that timestamp comparisons use tamper-proof data sources that cannot be manipulated
  through commit history manipulation or force pushes. Always verify that the timestamps
  being compared (such as PR updated_at vs comment created_at) come from authoritative
  sources that reflect actual...
repository: nuxt/nuxt
label: Security
language: Yaml
comments_count: 1
repository_stars: 57769
---

When implementing timing-based security checks in CI/CD workflows, ensure that timestamp comparisons use tamper-proof data sources that cannot be manipulated through commit history manipulation or force pushes. Always verify that the timestamps being compared (such as PR updated_at vs comment created_at) come from authoritative sources that reflect actual events rather than potentially forgeable commit metadata.

Example from GitHub workflows:
```yaml
- name: Get PR Info
  run: |
    pr="$(gh api /repos/${GH_REPO}/pulls/${PR_NUMBER})"
    updated_at="$(echo "$pr" | jq -r .updated_at)"
    # Use PR updated_at (push date) rather than commit timestamps
    # which could potentially be manipulated
    if [[ $(date -d $updated_at) > $(date -d $COMMENT_AT) ]]; then exit 1; fi
```

This prevents timing-based bypass attempts where an attacker might try to manipulate commit timestamps or use force pushes to circumvent security checks. The PR updated_at field represents the actual push date and cannot be forged through commit manipulation.