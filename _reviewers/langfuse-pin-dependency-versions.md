---
title: Pin dependency versions
description: 'Always pin external dependencies to specific versions in CI/CD workflows
  to ensure build reproducibility, stability, and security. This applies to:


  1. GitHub Actions (use tagged versions instead of branch names or commit SHAs)'
repository: langfuse/langfuse
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 13574
---

Always pin external dependencies to specific versions in CI/CD workflows to ensure build reproducibility, stability, and security. This applies to:

1. GitHub Actions (use tagged versions instead of branch names or commit SHAs)
2. External tools and binaries (specify exact versions when downloading)
3. Runtime environments (use specific versions in matrix configurations)

For GitHub Actions:
```yml
# ❌ Avoid:
- uses: pierotofy/set-swap-space@master
- uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1

# ✅ Prefer:
- uses: pierotofy/set-swap-space@v1.2.0
- uses: docker/login-action@v2
```

For external tools:
```yml
# ❌ Avoid:
curl -sSLo shfmt https://github.com/mvdan/sh/releases/latest/download/shfmt_linux_amd64

# ✅ Prefer:
curl -sSLo shfmt https://github.com/mvdan/sh/releases/download/v3.7.0/shfmt_linux_amd64
```

For runtime environments:
```yml
# ❌ Avoid:
node-version: [20]

# ✅ Prefer:
node-version: ["20.18.3"]
```

Using pinned versions ensures consistent builds across different environments and times, prevents unexpected breaking changes, and makes security audits more reliable.