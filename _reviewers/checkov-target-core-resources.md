---
title: Target core resources
description: When implementing network security checks for serverless functions like
  AWS Lambda, ensure you target the core function resources rather than just their
  endpoints. Security checks for configurations like CORS policies should be applied
  to the primary Lambda resources (`AWS::Lambda::Function`, `aws_lambda_function`)
  rather than only their URL interfaces...
repository: bridgecrewio/checkov
label: Networking
language: Yaml
comments_count: 2
repository_stars: 7668
---

When implementing network security checks for serverless functions like AWS Lambda, ensure you target the core function resources rather than just their endpoints. Security checks for configurations like CORS policies should be applied to the primary Lambda resources (`AWS::Lambda::Function`, `aws_lambda_function`) rather than only their URL interfaces (`AWS::Lambda::Url`, `aws_lambda_function_url`).

This ensures comprehensive coverage of potential security vulnerabilities across your serverless architecture.

Example correction:
```yaml
# Instead of:
value:
  - "AWS::Lambda::Url"

# Use:
value:
  - "AWS::Lambda::Function"
```

This approach applies across infrastructure-as-code platforms including CloudFormation and Terraform.