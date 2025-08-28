---
title: Design intuitive API interfaces
description: APIs should be designed with user experience in mind, accepting inputs
  in formats users naturally encounter and providing clear customization options with
  well-documented defaults.
repository: cloudflare/workers-sdk
label: API
language: Markdown
comments_count: 2
repository_stars: 3379
---

APIs should be designed with user experience in mind, accepting inputs in formats users naturally encounter and providing clear customization options with well-documented defaults.

When designing command-line interfaces or API endpoints:
- Accept natural input formats that users commonly work with (e.g., allowing GitHub URLs to be copied directly from the browser address bar)
- Provide customization options through clear parameter names (e.g., `--env-interface` to specify interface names)
- Always document default behaviors when parameters are omitted
- Use descriptive parameter names that clearly indicate their purpose

Example from CLI design:
```bash
# Good: Accepts natural GitHub URLs and provides clear customization
wrangler create my-app https://github.com/user/repo/tree/main/templates/worker
wrangler types --env-interface MyCustomEnv  # defaults to 'Env' if not specified
```

This approach reduces friction for users by eliminating the need to transform inputs into specific formats and provides flexibility while maintaining predictable default behavior.