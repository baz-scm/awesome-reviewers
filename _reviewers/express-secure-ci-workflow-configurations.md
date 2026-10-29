---
title: Secure CI workflow configurations
description: 'CI/CD workflow files (e.g., GitHub Actions) must be hardened against
  supply-chain and injection attacks since they often run with privileged access to
  secrets and repository write permissions. Specifically:'
repository: Expressjs/Express
label: Security
language: Yaml
comments_count: 2
repository_stars: 69580
---

CI/CD workflow files (e.g., GitHub Actions) must be hardened against supply-chain and injection attacks since they often run with privileged access to secrets and repository write permissions. Specifically:

1. Never reference third-party actions by a mutable tag (e.g., `@v1`). Pin them to an immutable, reviewed commit hash so an upstream compromise or malicious update cannot silently execute in your pipeline. Track and periodically review/update these pinned hashes.

2. Avoid the `pull_request_target` trigger when checking out PR code, since it grants the privileged base-repo token (including write access) to code that may come from an untrusted fork. Use `pull_request` instead, which runs with restricted, read-only permissions and cannot leak secrets or make privileged changes.

3. Scope any tokens/secrets passed to workflows or third-party actions to the minimum permissions and repositories needed (e.g., a fine-grained PAT limited to a single repo with only the required read/write scopes), rather than using broad or long-lived credentials.

4. Prefer reducing external action dependencies where practical—implementing simple logic (e.g., via `curl`/shell commands) instead of relying on a third-party action can shrink the attack surface and remove the need for hash-pinning maintenance altogether.

Example of a safer trigger configuration:
```yaml
on:
  pull_request:   # not pull_request_target
    branches: [main]
```

And pinning a third-party action:
```yaml
- uses: peter-evans/repository-dispatch@<full-commit-sha>  # not @v1
```</description>
</invoke>
