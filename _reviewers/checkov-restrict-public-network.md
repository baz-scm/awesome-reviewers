---
title: Restrict public network
description: Always configure cloud resources to restrict or disable public network
  access unless explicitly required for the application's functionality. Public network
  exposure increases the attack surface and should be minimized.
repository: bridgecrewio/checkov
label: Networking
language: Python
comments_count: 8
repository_stars: 7668
---

Always configure cloud resources to restrict or disable public network access unless explicitly required for the application's functionality. Public network exposure increases the attack surface and should be minimized.

Key implementation patterns to follow:

1. For cloud VMs and container instances:
   - Disable public IP address assignment
   - Example: Set `associate_public_ip_address` to false in AWS launch configurations

2. For storage and database services:
   - Enable block public access settings
   - Use private endpoints instead of public access
   - Example: Ensure `block_public_security_group_rules` is true for AWS EMR

3. For API and service endpoints:
   - Set public network access flags to 'disabled'
   - Configure 'deny' as the default network access action
   - Example: For Azure resources, set `public_network_access_enabled` to false

Code example showing proper implementation:
```python
from checkov.common.models.enums import CheckCategories
from checkov.terraform.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck

class AutoScalingGroupWithPublicAccess(BaseResourceNegativeValueCheck):
    def __init__(self):
        name = "Ensure AWS Auto Scaling group launch configuration doesn't have public IP address assignment enabled"
        id = "CKV_AWS_389"
        supported_resources = ['aws_launch_configuration']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_forbidden_values(self):
        return [True]

    def get_inspected_key(self):
        return "associate_public_ip_address"
```