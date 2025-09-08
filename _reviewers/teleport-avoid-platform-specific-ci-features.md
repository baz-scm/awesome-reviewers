---
title: avoid platform-specific CI features
description: Avoid using CI platform-specific features in workflows to prevent vendor
  lock-in and ensure portability. Instead of relying on GitHub Actions artifacts,
  Docker Hub registries, or other platform-specific storage mechanisms, use cloud-agnostic
  alternatives like S3 for artifact storage and transfer between jobs.
repository: gravitational/teleport
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 19109
---

Avoid using CI platform-specific features in workflows to prevent vendor lock-in and ensure portability. Instead of relying on GitHub Actions artifacts, Docker Hub registries, or other platform-specific storage mechanisms, use cloud-agnostic alternatives like S3 for artifact storage and transfer between jobs.

This approach ensures that workflows can be easily migrated between different CI platforms (GitHub Actions, GitLab CI, Jenkins, etc.) without requiring significant rewrites. It also provides better control over retention policies, access permissions, and integration with existing infrastructure.

Example of what to avoid:
```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: |
      ${{ github.workspace }}/build/artifacts
```

Preferred approach:
```yaml
- name: Upload artifacts to S3
  run: |
    aws s3 cp ${{ github.workspace }}/build/artifacts s3://your-bucket/artifacts/ --recursive
```

Additionally, consider consolidating sequential jobs to eliminate the need for intermediate artifact storage altogether, as this reduces both platform dependency and improves workflow efficiency.