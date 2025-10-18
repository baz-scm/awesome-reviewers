---
title: Contextualize documentation decisions
description: Documentation should provide contextual guidance about when and why to
  use features, not just how to configure them. Additionally, strategically link to
  external documentation rather than duplicating content to reduce maintenance overhead.
repository: sst/opencode
label: Documentation
language: Other
comments_count: 2
repository_stars: 28213
---

Documentation should provide contextual guidance about when and why to use features, not just how to configure them. Additionally, strategically link to external documentation rather than duplicating content to reduce maintenance overhead.

When documenting configuration options or features:
1. Explain the use cases that require each option
2. Provide context about when users would need specific settings
3. Link to authoritative external sources instead of duplicating their content

Example of good contextual documentation:
```markdown
## Azure URL Configuration

Different Azure deployments require different URL formats. Configure these options based on your deployment type:

| Deployment Type | useDeploymentBasedUrls | useCompletionUrls | Use Case |
|-----------------|------------------------|-------------------|----------|
| Standard API    | false                  | false             | Basic Azure OpenAI service |
| Custom Deployment | true                 | true              | When using named model deployments |

For detailed Azure setup instructions, see the [official Azure OpenAI documentation](https://docs.microsoft.com/azure/cognitive-services/openai/).
```

This approach helps users understand not just what to configure, but when they need each configuration, while avoiding the maintenance burden of duplicating external documentation.