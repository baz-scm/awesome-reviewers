---
title: Reusable documentation snippets
description: When writing integration guides or other docs that repeat common text
  (titles, step names, instructions like "Create an account + Generate an API Key"),
  pull that content from a shared snippets file (e.g. `/snippets/strings.mdx`) instead
  of hardcoding it in every page. This keeps wording consistent across dozens of similar
  guides and lets you update copy in...
repository: Helicone/helicone
label: Documentation
language: Other
comments_count: 3
repository_stars: 6248
---

When writing integration guides or other docs that repeat common text (titles, step names, instructions like "Create an account + Generate an API Key"), pull that content from a shared snippets file (e.g. `/snippets/strings.mdx`) instead of hardcoding it in every page. This keeps wording consistent across dozens of similar guides and lets you update copy in one place instead of editing every file individually.

Example:
```mdx
import { strings } from "/snippets/strings.mdx";

## {strings.howToIntegrate}

<Steps>
  <Step title={strings.generateKey}>
    <div dangerouslySetInnerHTML={{ __html: strings.generateKeyInstructions }} />
  </Step>

  <Step title={strings.setApiKey}>
    ```javascript
    HELICONE_API_KEY=<your-helicone-api-key>
    PROVIDER_API_KEY=<your-provider-api-key>
    ```
  </Step>

  <Step title={strings.modifyBasePath}>
    Replace the base URL with your provider endpoint and update the model name accordingly.
  </Step>
</Steps>
```

When adopting this pattern, double-check that no steps are dropped in the process — copy the full set of steps (account creation, setting keys, modifying the base path, etc.) so the guide remains complete and usable end-to-end, not just a partial template.</description>
</invoke>
