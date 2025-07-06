---
title: Comprehensive security scanning
description: 'Always configure security scanning tools with comprehensive coverage
  and readable output to maximize vulnerability detection. This includes:


  1. **Enable scanning across all files**: Use flags like `--enable-secret-scan-all-files`
  to ensure no potential vulnerability is missed.'
repository: bridgecrewio/checkov
label: Security
language: Yaml
comments_count: 3
repository_stars: 7667
---

Always configure security scanning tools with comprehensive coverage and readable output to maximize vulnerability detection. This includes:

1. **Enable scanning across all files**: Use flags like `--enable-secret-scan-all-files` to ensure no potential vulnerability is missed.

2. **Configure Docker-based scanners with proper TTY support**: When running security tools in containers, add the `--tty` flag for better output handling and readability.

3. **Enable appropriate protection mechanisms**: Ensure protective measures like Web Application Firewalls are properly configured in your infrastructure code.

Example:
```yaml
# Pre-commit hook with proper configuration
-   id: checkov_secrets
    name: Checkov Secrets
    description: This hook looks for secrets with checkov.
    entry: checkov -d . --framework secrets --enable-secret-scan-all-files

-   id: checkov_container
    name: Checkov
    description: This hook runs checkov.
    entry: bridgecrew/checkov:latest --tty -d .
```

When writing infrastructure as code, ensure that protection mechanisms like WAF are explicitly enabled:
```python
aws_cdk.aws_cloudfront.CfnDistribution(
    distribution_config={"webAclId": my_web_acl_id}
)
```

These practices help ensure that security vulnerabilities are consistently detected and addressed before deployment.