---
title: Mask sensitive tokens
description: Always mask sensitive tokens, credentials, and secrets in CI/CD workflows
  to prevent accidental exposure in logs or build outputs. In GitHub Actions, use
  the `::add-mask::` command before outputting or storing sensitive values in environment
  variables.
repository: astral-sh/uv
label: Security
language: Yaml
comments_count: 1
repository_stars: 60322
---

Always mask sensitive tokens, credentials, and secrets in CI/CD workflows to prevent accidental exposure in logs or build outputs. In GitHub Actions, use the `::add-mask::` command before outputting or storing sensitive values in environment variables.

Example:
```yaml
- name: "Get AWS CodeArtifact token"
  run: |
    UV_TEST_AWS_TOKEN=$(aws codeartifact get-authorization-token \
      --domain tests \
      --domain-owner ${{ secrets.AWS_ACCOUNT_ID }} \
      --region us-east-1 \
      --query authorizationToken \
      --output text)
    echo "::add-mask::$UV_TEST_AWS_TOKEN"
    echo "UV_TEST_AWS_TOKEN=$UV_TEST_AWS_TOKEN" >> $GITHUB_ENV
```

This practice should be applied consistently for all types of authentication tokens (AWS, GCP, API keys, etc.) to maintain security and prevent credential leakage. Even in private repositories, proper token masking is essential for security best practices and to prevent credentials from being visible in workflow logs that team members can access.