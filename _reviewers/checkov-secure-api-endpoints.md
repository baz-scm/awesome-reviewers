---
title: Secure API endpoints
description: Always configure proper authorization for API endpoints to prevent unauthorized
  access to back-end resources. Avoid combinations that create open access, such as
  using `AuthorizationType.NONE` together with `api_key_required=False` in API Gateway
  configurations.
repository: bridgecrewio/checkov
label: API
language: Yaml
comments_count: 2
repository_stars: 7667
---

Always configure proper authorization for API endpoints to prevent unauthorized access to back-end resources. Avoid combinations that create open access, such as using `AuthorizationType.NONE` together with `api_key_required=False` in API Gateway configurations.

Remember that keyword argument order can vary in function calls, so ensure your security checks account for all possible parameter arrangements. For example, in AWS CDK:

```python
# Insecure configuration - will create an open endpoint
aws_cdk.aws_apigateway.Method(
    resource,
    http_method="GET",
    integration=some_integration,
    authorization_type=aws_cdk.aws_apigateway.AuthorizationType.NONE,
    api_key_required=False
)

# Secure configuration
aws_cdk.aws_apigateway.Method(
    resource,
    http_method="GET",
    integration=some_integration,
    authorization_type=aws_cdk.aws_apigateway.AuthorizationType.IAM,  # Or other appropriate type
    api_key_required=True  # When applicable
)
```

Additionally, define security configurations at the appropriate level in API specifications to avoid redundancy while ensuring comprehensive protection.