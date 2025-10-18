---
title: require explicit security consent
description: Always require explicit user consent and validation before executing
  potentially dangerous operations, especially those involving external configuration
  or dynamic user inputs. This prevents security vulnerabilities from being introduced
  through seemingly innocent features.
repository: jj-vcs/jj
label: Security
language: Rust
comments_count: 2
repository_stars: 21171
---

Always require explicit user consent and validation before executing potentially dangerous operations, especially those involving external configuration or dynamic user inputs. This prevents security vulnerabilities from being introduced through seemingly innocent features.

For external configuration (like repo-provided settings), implement a trust model that forces users to explicitly review and approve dangerous settings rather than silently executing them. As noted in the discussions: "If we do let repos set dangerous settings then we should certainly have a trust model for it."

For user inputs in templates or dynamic systems, avoid allowing arbitrary string interpolation that could lead to injection vulnerabilities. Consider restricting to literal strings or implementing strict validation, since "dealing with dynamic template strings is a known problem spot in basically every language (c.f. printf vulnerabilities in C, etc)."

Example approach for configuration:
```rust
// Bad: Silently execute repo config
load_and_execute_repo_config();

// Good: Require explicit user consent
if user_explicitly_trusts_repo_config() {
    load_and_execute_repo_config();
} else {
    show_diff_and_prompt_for_approval();
}
```

The key principle is that downloading files should never be implicit consent to execute arbitrary code, and systems should be secure by default rather than relying on users to exercise unrealistic caution.