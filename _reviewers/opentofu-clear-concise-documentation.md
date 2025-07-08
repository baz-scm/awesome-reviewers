---
title: Clear concise documentation
description: 'Write documentation that is direct, consistent, and appropriately detailed.
  Follow these principles:


  1. **Use direct language** - Prefer straightforward assertions over gentle phrasing.
  Instead of "Please be cautious when..." use "Use caution when..." or simply state
  facts and instructions directly.'
repository: opentofu/opentofu
label: Documentation
language: Other
comments_count: 5
repository_stars: 25901
---

Write documentation that is direct, consistent, and appropriately detailed. Follow these principles:

1. **Use direct language** - Prefer straightforward assertions over gentle phrasing. Instead of "Please be cautious when..." use "Use caution when..." or simply state facts and instructions directly.

2. **Maintain consistent structure** - Place similar elements (notes, warnings, etc.) in the same position across documents. For example, place note sections consistently within the "Usage" section of command documentation.

3. **Format for readability** - For terminal output examples, use consistent formatting with line markers (like │) and limit width to approximately 72 columns to prevent horizontal scrolling:

```
Error: Provider instance not present
│
│ To work with aws_cloudwatch_log_group.lambda_cloudfront["sa-east-1"] its original provider instance at
│ provider["registry.opentofu.org/hashicorp/aws"].by_region["sa-east-1"] is required, but it has been removed.
```

4. **Avoid unnecessary examples** - Only include examples that provide significant context or clarity. Remove content that increases complexity without adding value.

5. **Balance detail with brevity** - Keep documentation concise since readers tend to skip overly long sections. Include essential information while avoiding excessive detail that can overwhelm users.