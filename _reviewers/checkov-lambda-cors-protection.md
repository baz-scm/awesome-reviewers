---
title: Lambda CORS protection
description: When implementing network security checks for AWS Lambda functions, ensure
  that CORS (Cross-Origin Resource Sharing) policies are verified on the core Lambda
  function resources, not just on function URL endpoints. This prevents open CORS
  policies that could expose your Lambda functions to unauthorized cross-origin requests.
repository: bridgecrewio/checkov
label: Networking
language: Yaml
comments_count: 2
repository_stars: 7667
---

When implementing network security checks for AWS Lambda functions, ensure that CORS (Cross-Origin Resource Sharing) policies are verified on the core Lambda function resources, not just on function URL endpoints. This prevents open CORS policies that could expose your Lambda functions to unauthorized cross-origin requests.

For proper implementation, target these resource types:
- In CloudFormation: `AWS::Lambda::Function` (not just `AWS::Lambda::Url`)
- In Terraform: `aws_lambda_function` (not just `aws_lambda_function_url`)

Example configuration for a security check:
```yaml
metadata:
  name: "Ensure no open CORS policy"
  id: "CKV2_AWS_XX"
  category: "NETWORKING"
scope:
  provider: "aws"
definition:
  and:
    - cond_type: "filter"
      attribute: "resource_type"
      value:
        - "AWS::Lambda::Function"  # Core Lambda resource
        # - "AWS::Lambda::Url"     # Not sufficient alone
```