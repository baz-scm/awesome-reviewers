---
title: Parameterize security commands
description: When writing security-related CLI commands or remediation steps, always
  use standardized parameter placeholders (e.g., `<REGION>`, `<RESOURCE_NAME>`) instead
  of hardcoded values. This practice ensures commands are adaptable across different
  environments, prevents implementation errors, and makes security remediation steps
  more reliable. Properly...
repository: prowler-cloud/prowler
label: Security
language: Json
comments_count: 4
repository_stars: 11834
---

When writing security-related CLI commands or remediation steps, always use standardized parameter placeholders (e.g., `<REGION>`, `<RESOURCE_NAME>`) instead of hardcoded values. This practice ensures commands are adaptable across different environments, prevents implementation errors, and makes security remediation steps more reliable. Properly parameterized commands also improve documentation and enable automation scripts to be more flexible and reusable.

Example:
```bash
# Incorrect (hardcoded values)
aws lambda remove-permission --region us-east-1 --function-name cc-process-app-queue --statement-id FullAccess

# Correct (parameterized)
aws lambda remove-permission --region <REGION> --function-name <FUNCTION_NAME> --statement-id FullAccess
```