---
title: Provider instance management
description: Ensure proper configuration of provider instances when using environment-specific
  settings. When using `for_each` with providers, carefully manage the lifecycle of
  provider instances to avoid warnings or errors during resource operations.
repository: opentofu/opentofu
label: Configurations
language: Other
comments_count: 2
repository_stars: 25901
---

Ensure proper configuration of provider instances when using environment-specific settings. When using `for_each` with providers, carefully manage the lifecycle of provider instances to avoid warnings or errors during resource operations.

Key considerations:
1. Provider instances created with `for_each` must remain available for the entire lifecycle of any resources using them, including during destruction
2. When resources also use `for_each`, ensure their instance keys don't exactly match the provider's to allow proper resource removal
3. Use selective filtering when creating resource instances to maintain needed provider instances

```hcl
# Good practice: Filter resources but maintain provider instances
variable "aws_regions" {
  type = map(object({
    vpc_cidr_block = string
  }))
}

provider "aws" {
  alias    = "by_region"
  for_each = var.aws_regions

  region = each.key
}

resource "aws_vpc" "private" {
  # Filter var.aws_regions to include only non-null elements
  # allowing provider instances to remain while removing resources
  for_each = {
    for region, config in var.aws_regions : region => config
    if config != null
  }
  provider = aws.by_region[each.key]

  cidr_block = each.value.vpc_cidr_block
}
```

This pattern allows you to "disable" resources in specific regions by setting their config to null while maintaining the provider instance needed for cleanup operations. Without this approach, OpenTofu would generate warnings when trying to destroy resources whose provider instances have been removed.