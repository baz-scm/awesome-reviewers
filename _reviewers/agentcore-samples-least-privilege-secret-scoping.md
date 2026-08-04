---
title: Least-privilege secret scoping
description: When granting IAM access to Secrets Manager, avoid broad resource wildcards
  (e.g., `arn:aws:secretsmanager:...:secret:*`). Prefer narrowing by the exact secret
  ARN(s) or by a well-known secret-name prefix for the specific service/feature. Also
  remove redundant policy constraints that don’t add additional security beyond what
  the ARN already enforces.
repository: awslabs/agentcore-samples
label: Security
language: Shell
comments_count: 1
repository_stars: 3244
---

When granting IAM access to Secrets Manager, avoid broad resource wildcards (e.g., `arn:aws:secretsmanager:...:secret:*`). Prefer narrowing by the exact secret ARN(s) or by a well-known secret-name prefix for the specific service/feature. Also remove redundant policy constraints that don’t add additional security beyond what the ARN already enforces.

Example (tighten wildcard to a prefix when possible):
```sh
# Prefer a scoped prefix over secret:* (example pattern)
# resource: arn:aws:secretsmanager:*:${ACCOUNT_ID}:secret:agentcore-payments/*

secretsmanager_policy() {
  jq -n --arg accountId "$ACCOUNT_ID" --arg secretPrefix "agentcore-payments/" '
  {
    Version: "2012-10-17",
    Statement: [{
      Sid: "AllowScopedSecretStorage",
      Effect: "Allow",
      Action: [
        "secretsmanager:CreateSecret",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UpdateSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:DeleteSecret",
        "secretsmanager:DescribeSecret",
        "secretsmanager:TagResource"
      ],
      Resource: [
        ("arn:aws:secretsmanager:*:" + $accountId + ":secret:" + $secretPrefix + "*")
      ]
    }]
  }'
}
```

If a content scan flags a wildcard, address it by tightening the resource scope (prefix/ARN/tag-based condition) rather than keeping extra conditions that are functionally redundant.