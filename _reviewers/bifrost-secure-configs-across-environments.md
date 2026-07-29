---
title: Secure configs across environments
description: When making security-related changes, ensure the configuration is (1)
  least-privilege/scoped, (2) actually enforced by the platform, and (3) consistent
  across code/docs.
repository: maximhq/bifrost
label: Security
language: Yaml
comments_count: 4
repository_stars: 6862
---
{% raw %}
When making security-related changes, ensure the configuration is (1) least-privilege/scoped, (2) actually enforced by the platform, and (3) consistent across code/docs.

Apply this standard:
- Scope secrets/tokens narrowly: don’t add sensitive tokens to release/runtime job env unless the release jobs truly need them. Prefer using them only in dedicated test/integration jobs.
- Make non-root enforcement verifiable: if you set `runAsNonRoot: true`, the kubelet must be able to verify the container’s non-root user. Avoid cases where the image uses a non-numeric/named `USER`.
- Use numeric UIDs for `USER` when `runAsNonRoot` is enabled (or ensure the platform can otherwise verify). If you need deterministic behavior across k8s distros, set a numeric UID in the Dockerfile, and align `podSecurityContext` with your storage-class behavior.
- Validate Helm rendering/merge behavior: changes like switching `podSecurityContext` to `{}` can behave unexpectedly due to Helm map merges—always confirm the rendered `securityContext` with `helm template`.
- Keep security defaults in schema/docs aligned with code: don’t adjust documented defaults without updating the code default, especially for auth/security parameters.

Example (numeric UID to satisfy kubelet verification):
```dockerfile
# Ensure kubelet can verify non-root when runAsNonRoot: true
USER 1000:0
```

Example (scope secrets to test jobs):
```yaml
# Only provide sensitive tokens where they are required (e.g., PR test jobs)
# Avoid injecting tokens into broad release job env blocks.
env:
  # GITHUB_COPILOT_TOKEN: ${{ secrets.GITHUB_COPILOT_TOKEN }}  # keep out of release jobs
```
{% endraw %}
