---
title: Local configuration exclusion
description: Exclude personal and local configuration files from version control while
  ensuring they are properly handled during environment setup. Personal configurations
  should use patterns like `*.local.*` or be placed in designated directories that
  are gitignored to prevent accidental commits of developer-specific settings.
repository: PostHog/posthog
label: Configurations
language: Other
comments_count: 2
repository_stars: 28460
---

Exclude personal and local configuration files from version control while ensuring they are properly handled during environment setup. Personal configurations should use patterns like `*.local.*` or be placed in designated directories that are gitignored to prevent accidental commits of developer-specific settings.

When setting up new environments or worktrees, be explicit about which configuration files to copy. Use specific patterns rather than wildcards to avoid copying unintended files.

Example:
```bash
# In .gitignore
bin/mprocs*.local.yaml
.env.local
playground/

# In setup scripts - be specific about what to copy
if [[ -f "${main_repo}/.env" ]]; then
    cp "${main_repo}/.env" "${worktree_path}/"
fi
# Rather than copying all .env* files indiscriminately
```

This prevents personal development configurations from polluting the shared codebase while ensuring consistent environment setup across different development contexts.