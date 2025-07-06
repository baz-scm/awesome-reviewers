---
title: Document configuration options
description: 'Always provide comprehensive documentation for all configuration options,
  including environment variables, feature flags, and version overrides. For each
  configuration option:'
repository: bridgecrewio/checkov
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 7668
---

Always provide comprehensive documentation for all configuration options, including environment variables, feature flags, and version overrides. For each configuration option:

1. Specify default values and all possible values
2. Include examples showing both default and custom settings
3. Document the correct syntax for the configuration format
4. Group related configurations together for better discoverability

For environment variables used for authentication:

```yaml
| Variable Name     | Description                                                    | Default Value    |
|-------------------|----------------------------------------------------------------|------------------|
| TF_HOST_NAME      | Terraform Enterprise host name (example.com)                   | app.terraform.io |
| TF_REGISTRY_TOKEN | Private registry access token for Terraform Cloud/Enterprise   | None             |
```

When defining multiple configuration options in JSON files, use arrays for multiple values with the same key:

```json
{
  "name": "my-package",
  "version": "1.0.0",
  "//": ["checkov:skip=express[BC_LIC_2]: ignore license violations",
         "checkov:skip=CVE-2023-123: ignore this CVE"]
}
```

For container-based tools, document version pinning options:

```yaml
# Default configuration uses 'latest' tag
hooks:
  - id: checkov_container
    entry: bridgecrew/checkov -d .

# Override with specific version
hooks:
  - id: checkov_container
    entry: bridgecrew/checkov:2.4.2 -d .
```