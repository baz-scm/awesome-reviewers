---
title: document workflow capabilities
description: Workflow methods should include comments that document their orchestration
  capabilities and data access patterns. This helps developers understand the available
  temporal execution features and interaction methods.
repository: cloudflare/workers-sdk
label: Temporal
language: JavaScript
comments_count: 2
repository_stars: 3379
---

Workflow methods should include comments that document their orchestration capabilities and data access patterns. This helps developers understand the available temporal execution features and interaction methods.

Key areas to document:
- Data access patterns (bindings via `this.env`, parameters via `event.payload`)
- Orchestration capabilities (waiting for external events, human approval, webhooks)
- External interaction endpoints (HTTP POST patterns for submitting data to workflow instances)

Example:
```javascript
async run(event, step) {
    // Can access bindings on `this.env`
    // Can access params on `event.payload`
    
    const files = await step.do("my first step", async () => {
        // Fetch a list of files from $SOME_SERVICE
        return { files: [...] };
    });
    
    // You can optionally have a Workflow wait for additional data,
    // human approval or an external webhook or HTTP request before progressing.
    // You can submit data via HTTP POST to /accounts/{account_id}/workflows/{workflow_name}/instances/{instance_id}/events/{eventName}
}
```

This documentation pattern ensures workflow code is self-explanatory about its durable execution capabilities and helps maintain clarity in complex orchestration scenarios.