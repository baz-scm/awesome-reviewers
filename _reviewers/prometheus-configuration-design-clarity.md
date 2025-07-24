---
title: Configuration design clarity
description: Design configuration options to be unambiguous and self-documenting.
  Avoid reusing the same configuration field for different data types, as this creates
  confusion and maintenance burden. Instead, use explicit indicators or separate fields
  to handle different scenarios. Make mutual exclusivity and constraints between configuration
  options explicit in both...
repository: prometheus/prometheus
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 59616
---

Design configuration options to be unambiguous and self-documenting. Avoid reusing the same configuration field for different data types, as this creates confusion and maintenance burden. Instead, use explicit indicators or separate fields to handle different scenarios. Make mutual exclusivity and constraints between configuration options explicit in both documentation and validation. Minimize duplication by designing unified approaches that work across similar use cases.

Example of problematic design:
```yaml
# Avoid: Same field accepting different types
environment: <string|AzureCloudConfig>
```

Example of clearer design:
```yaml
# Better: Use explicit indicator
environment: <string> # Use "custom" to enable custom_config
custom_config: <AzureCloudConfig> # Only used when environment="custom"
```

For mutually exclusive options, make the constraint explicit:
```yaml
# Clear constraint documentation
promote_resource_attributes: [<string>, ...] # Cannot be used with promote_all_resource_attributes
promote_all_resource_attributes: <boolean> # Cannot be used with promote_resource_attributes
ignore_resource_attributes: [<string>, ...] # Only valid when promote_all_resource_attributes=true
```