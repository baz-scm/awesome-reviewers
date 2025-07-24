---
title: avoid GitHub template injection
description: Avoid using GitHub workflow template expressions `${{ }}` directly in
  shell commands within `run:` steps, as this can lead to template injection vulnerabilities.
  Untrusted input like branch names, PR titles, or commit messages can be crafted
  to execute arbitrary code since GitHub template expansion happens before workflow
  execution.
repository: prometheus/prometheus
label: Security
language: Yaml
comments_count: 1
repository_stars: 59616
---

Avoid using GitHub workflow template expressions `${{ }}` directly in shell commands within `run:` steps, as this can lead to template injection vulnerabilities. Untrusted input like branch names, PR titles, or commit messages can be crafted to execute arbitrary code since GitHub template expansion happens before workflow execution.

Instead, pass GitHub context values through environment variables and use shell variable expansion `${...}` to access them safely. This ensures the values are treated as literal strings rather than executable code.

Example of vulnerable code:
```yaml
- run: ./script.sh "$(./get_version.sh ${{ github.ref_name }})"
```

Secure alternative:
```yaml
- run: ./script.sh "$(./get_version.sh ${GH_REF_NAME})"
  env:
    GH_REF_NAME: ${{ github.ref_name }}
```

This pattern is especially critical for workflows that can be triggered by external contributors or when processing any user-controllable input from GitHub context variables.