---
title: audit third-party dependencies
description: Before using third-party actions, libraries, or dependencies that require
  access to sensitive data (tokens, secrets, credentials), conduct a thorough security
  audit. Third-party code, especially when source is obfuscated or built/compiled,
  poses significant security risks when granted access to sensitive resources.
repository: cloudflare/workers-sdk
label: Security
language: Yaml
comments_count: 1
repository_stars: 3379
---

Before using third-party actions, libraries, or dependencies that require access to sensitive data (tokens, secrets, credentials), conduct a thorough security audit. Third-party code, especially when source is obfuscated or built/compiled, poses significant security risks when granted access to sensitive resources.

Key evaluation steps:
1. **Review source code transparency** - Prefer dependencies with clear, readable source code over those with built/compiled distributions
2. **Apply principle of least privilege** - Use tokens with minimal required permissions (e.g., read:org only tokens instead of broader access)
3. **Consider alternatives** - Evaluate copying source code into your own codebase or forking the dependency into your organization's control
4. **Assess maintenance and reputation** - Review the dependency's maintenance status, contributor history, and community trust

Example from GitHub Actions:
```yaml
# Instead of using third-party action with broad token
- uses: third-party/action@v1
  with:
    GITHUB_TOKEN: ${{ secrets.GH_ACCESS_TOKEN }}

# Consider forking to your org or copying source code
- uses: your-org/forked-action@v1
  with:
    GITHUB_TOKEN: ${{ secrets.LIMITED_READ_TOKEN }}
```

When in doubt, prioritize security over convenience by maintaining direct control over code that accesses sensitive resources.