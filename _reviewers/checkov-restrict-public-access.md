---
title: Restrict public access
description: Cloud resources should be configured to restrict public network access
  by default to minimize potential attack surfaces. Always explicitly disable public-facing
  endpoints and network interfaces unless absolutely necessary for the service to
  function.
repository: bridgecrewio/checkov
label: Networking
language: Python
comments_count: 10
repository_stars: 7667
---

Cloud resources should be configured to restrict public network access by default to minimize potential attack surfaces. Always explicitly disable public-facing endpoints and network interfaces unless absolutely necessary for the service to function.

When implementing security checks for cloud resources:

1. Use appropriate base classes like `BaseResourceValueCheck` or `BaseResourceNegativeValueCheck` to verify public access is disabled
2. Check the correct property paths in configuration (e.g., `public_network_access_enabled`, `associate_public_ip_address`)
3. Handle default values correctly - many cloud resources enable public access by default
4. Validate all network-facing attributes (ports, protocols, IP ranges)

Example for AWS EMR:
```python
from checkov.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from checkov.common.models.enums import CheckCategories

class EMRPubliclyAccessible(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure AWS EMR block public access setting is enabled"
        id = "CKV_AWS_390"
        supported_resources = ['aws_emr_block_public_access_configuration']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "block_public_security_group_rules"
```

For VM instances, database services, storage accounts, and container services, ensure you're checking all network access points including public IPs, public endpoints, network rules, and default access policies.