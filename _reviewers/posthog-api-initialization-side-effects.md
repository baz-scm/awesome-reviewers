---
title: API initialization side effects
description: When initializing API clients, prefer bootstrap/configuration patterns
  over method calls that may trigger unintended side effects like billing events,
  data capture, or state changes. Method calls during initialization can have unexpected
  consequences that users may not anticipate or want to pay for.
repository: PostHog/posthog
label: API
language: Html
comments_count: 2
repository_stars: 28460
---

When initializing API clients, prefer bootstrap/configuration patterns over method calls that may trigger unintended side effects like billing events, data capture, or state changes. Method calls during initialization can have unexpected consequences that users may not anticipate or want to pay for.

Instead of calling methods like `identify()`, `capture()`, or similar action-triggering functions during client setup, use configuration objects, bootstrap data, or initialization parameters to achieve the same result without side effects.

Example of problematic initialization:
```javascript
// This triggers an identify event that users get billed for
posthog.init(token, config);
posthog.identify(distinctId); // Captures billable event
```

Preferred approach using bootstrap configuration:
```javascript
// This achieves the same result without capturing events
const config = {
    api_host: projectConfig.api_host,
    bootstrap: {
        distinctId: distinctId // Set identity without triggering events
    }
};
posthog.init(token, config);
```

This pattern ensures that client initialization only sets up the necessary state without triggering actions that have business implications or costs. Always consider whether initialization methods have side effects and prefer declarative configuration approaches when available.