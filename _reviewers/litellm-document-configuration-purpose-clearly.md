---
title: Document configuration purpose clearly
description: When documenting configuration features, always provide clear explanations
  of their purpose, use cases, and how they map to underlying parameters. Users should
  understand not just how to use a configuration option, but why they would want to
  use it and what problem it solves.
repository: BerriAI/litellm
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 28310
---

When documenting configuration features, always provide clear explanations of their purpose, use cases, and how they map to underlying parameters. Users should understand not just how to use a configuration option, but why they would want to use it and what problem it solves.

For environment variables, explicitly document the mapping between environment variables and configuration parameters:

```markdown
## Environment Variables

The Heroku provider is aware of the following config variables:

- `HEROKU_API_KEY`: This value corresponds to the [`api_key` param](https://docs.litellm.ai/docs/set_keys#litellmapi_key). Set this to the value of Heroku's `INFERENCE_KEY` config variable.
- `HEROKU_API_BASE`: This value corresponds to the [`api_base` param](https://docs.litellm.ai/docs/set_keys#litellmapi_base). Set this to the value of Heroku's `INFERENCE_URL` config variable.
```

For configuration features that may have non-obvious use cases, include practical scenarios:

```markdown
#### Import Models

Import models from a YAML file. This is useful when migrating models from a self-hosted instance to a cloud instance, allowing you to gradually port your existing configuration.
```

This prevents confusion and reduces the need for clarifying questions about the purpose and intended workflow of configuration features.