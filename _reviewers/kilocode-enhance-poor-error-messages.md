---
title: enhance poor error messages
description: When external APIs or dependencies provide cryptic or unhelpful error
  messages, wrap them with user-friendly, actionable guidance. This is especially
  important when the external service returns terse responses that don't help users
  understand what went wrong or how to fix it.
repository: kilo-org/kilocode
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 7302
---

When external APIs or dependencies provide cryptic or unhelpful error messages, wrap them with user-friendly, actionable guidance. This is especially important when the external service returns terse responses that don't help users understand what went wrong or how to fix it.

Transform generic errors into specific, step-by-step instructions that guide users toward resolution. Include relevant links, configuration steps, or troubleshooting information.

Example:
```typescript
// Instead of letting cryptic API errors bubble up
if (!this.options.fireworksApiKey) {
    yield {
        type: "text",
        text: "ERROR: Fireworks API key is required but was not provided.\n\n" +
              "Please set your API key in the extension settings:\n" +
              "1. Open the KiloCode settings panel\n" +
              "2. Select 'Fireworks' as your provider\n" +
              "3. Enter your API key\n\n" +
              "You can get your API key from: https://fireworks.ai/account/api-keys",
    }
    return
}
```

This approach is justified when external services provide inadequate error context (like Fireworks returning just `{"error":"unauthorized"}` instead of OpenAI's detailed error messages). The enhanced messages should be implemented at the API boundary to avoid duplicating error handling logic throughout the codebase.