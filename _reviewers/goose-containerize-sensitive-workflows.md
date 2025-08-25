---
title: containerize sensitive workflows
description: Use containerization to isolate operations that could access sensitive
  data, modify critical systems, or execute untrusted code. Containers provide a secure
  boundary that prevents workflows from affecting the host environment or accessing
  resources beyond their intended scope.
repository: block/goose
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 19037
---

Use containerization to isolate operations that could access sensitive data, modify critical systems, or execute untrusted code. Containers provide a secure boundary that prevents workflows from affecting the host environment or accessing resources beyond their intended scope.

This practice is essential when:
- Running automated security scans or code analysis in CI/CD pipelines
- Testing new features that modify data or system state
- Executing user-contributed code or recipes
- Building and testing in environments that need to remain isolated from production systems

Example implementation:
```yaml
# GitHub Actions workflow
- name: Scan recipes in isolation
  run: |
    docker run --rm \
      --network none \
      --read-only \
      -v $(pwd)/recipes:/recipes:ro \
      recipe-scanner:latest \
      scan /recipes
```

```bash
# Development workflow
container-use stdio
# Run a container agent to add a feature to save my to-do list data in sqlite, 
# build and run tests, but use a separate Git branch so my main code stays safe.
```

Always prefer containerized execution over direct host execution when dealing with potentially unsafe operations, ensuring that failures or security issues remain contained within the isolated environment.