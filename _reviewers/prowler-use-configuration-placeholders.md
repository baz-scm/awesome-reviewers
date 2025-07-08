---
title: Use configuration placeholders
description: 'Avoid hardcoding specific values like regions, timeframes, or identifiers
  in configuration commands, examples, or settings. Instead, use descriptive placeholders
  that clearly indicate the type of value required. This practice:'
repository: prowler-cloud/prowler
label: Configurations
language: Json
comments_count: 3
repository_stars: 11834
---

Avoid hardcoding specific values like regions, timeframes, or identifiers in configuration commands, examples, or settings. Instead, use descriptive placeholders that clearly indicate the type of value required. This practice:

1. Makes configuration examples more reusable across different environments
2. Prevents users from mistakenly using example values in production
3. Supports parametrization of values that may change across environments or over time

**Example - Instead of:**
```
aws dms modify-replication-instance --region us-east-1 --replication-instance-arn arn:aws:dms:us-east-1:123456789012:rep:ABCDABCDABCDABCDABCDABCDAB --auto-minor-version-upgrade --apply-immediately
```

**Use:**
```
aws dms modify-replication-instance --region <REGION> --replication-instance-arn <REPLICATION_INSTANCE_ARN> --auto-minor-version-upgrade --apply-immediately
```

Similarly, when defining configurable timeframes or identifiers in code, make them parameters rather than hardcoding values like "6 months" or specific domain GUIDs. This approach improves flexibility, reusability, and reduces potential confusion about whether example values are required literals.