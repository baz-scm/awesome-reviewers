---
title: Provide contextual error messages
description: Error messages should include specific context about what went wrong
  and provide actionable guidance for resolution. Avoid generic error messages that
  leave developers guessing about the root cause or solution.
repository: browserbase/stagehand
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 16443
---

Error messages should include specific context about what went wrong and provide actionable guidance for resolution. Avoid generic error messages that leave developers guessing about the root cause or solution.

When throwing errors:
1. Include the original error details when wrapping exceptions to preserve debugging information
2. Provide specific context about the current state or operation that failed
3. Offer clear, actionable steps the developer can take to resolve the issue

Example of improved error messaging:

```typescript
// Poor: Generic error message
throw new Error("act() is not implemented on the base page object");

// Better: Contextual error with actionable guidance
throw new Error(
  "act() is not implemented on the base page object. Ensure you are calling init() on the Stagehand object before calling methods on the page object."
);

// Best: Include original error details when wrapping
constructor(error?: unknown) {
  if (error instanceof Error || error instanceof StagehandError) {
    super(
      `\nHey! We're sorry you ran into an error. \nIf you need help, please open a Github issue or reach out to us on Slack: https://stagehand.dev/slack\n\nFull error:\n${error.message}`
    );
  }
}
```

This approach reduces debugging time and improves the developer experience by making failures self-explanatory.