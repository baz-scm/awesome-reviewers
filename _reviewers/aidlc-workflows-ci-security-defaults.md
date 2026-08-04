---
title: CI Security Defaults
description: 'Default CI/security configuration to minimize risk while keeping automated
  findings meaningful.


  Apply these rules:

  1) Enforce least-privilege GitHub Actions permissions'
repository: awslabs/aidlc-workflows
label: Security
language: Yaml
comments_count: 2
repository_stars: 3849
---

Default CI/security configuration to minimize risk while keeping automated findings meaningful.

Apply these rules:
1) Enforce least-privilege GitHub Actions permissions
- In every workflow, start from deny-all unless you can justify additional scopes.
- Use `permissions: {}` in the workflow to ensure the token has no default capabilities.

Example:
```yml
permissions: {}
```

2) Treat security scanner results as actionable—exclude only confirmed non-issues
- If a tool rule repeatedly flags a pattern that is intentionally safe in your codebase (e.g., type-narrowing `assert`s used only to satisfy type checking), exclude the specific rule(s) rather than disabling scanning broadly.
- Keep exclusions narrow and reviewable.

Example:
```yml
semgrep scan \
  --oss-only --verbose --metrics=off --config=r/all \
  --exclude-rule <tool.rule-id-1> \
  --exclude-rule <tool.rule-id-2>
```

Result: workflows don’t grant unnecessary token privileges, and security scanning stays high-signal by suppressing only verified false positives/irrelevant checks.