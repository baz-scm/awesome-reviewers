---
title: Include descriptive documentation
description: Provide complete, clear descriptions for all configuration elements in
  documentation. Every output, variable, argument, and configuration option should
  include descriptive text explaining its purpose, requirements, and usage from the
  consumer's perspective.
repository: hashicorp/terraform
label: Documentation
language: Other
comments_count: 5
repository_stars: 45532
---

Provide complete, clear descriptions for all configuration elements in documentation. Every output, variable, argument, and configuration option should include descriptive text explaining its purpose, requirements, and usage from the consumer's perspective.

When documenting outputs, always include a description field:

```hcl
output "website_url" {
  value = "https://${module.web_server.instance_ip_addr}"
  description = "The website URL, starting with https://"
}

output "db_password" {
  value     = aws_db_instance.db.password
  sensitive = true
  description = "The database password."
}
```

For configuration instructions, be explicit rather than implicit. When explaining how to use a feature, provide clear steps and concrete examples showing the correct implementation. Replace vague terms with specific descriptions that help readers understand exactly what actions to take.

Documentation should follow a consistent pattern with proper introduction sentences for each section, and use present tense rather than future tense. Address users directly with clear, actionable language that guides them through proper implementation.