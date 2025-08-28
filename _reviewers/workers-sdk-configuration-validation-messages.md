---
title: Configuration validation messages
description: Ensure configuration validation provides clear, actionable error messages
  that guide users toward correct configuration. Validation should be comprehensive,
  checking not only types but also value ranges, logical consistency, and edge cases
  like undefined vs explicitly set values.
repository: cloudflare/workers-sdk
label: Configurations
language: TypeScript
comments_count: 13
repository_stars: 3379
---

Ensure configuration validation provides clear, actionable error messages that guide users toward correct configuration. Validation should be comprehensive, checking not only types but also value ranges, logical consistency, and edge cases like undefined vs explicitly set values.

When validating configuration:
- Provide specific error messages that include the expected format and actual received value
- Include examples of valid configuration when possible
- Handle edge cases like undefined values explicitly rather than assuming they're equivalent to false/empty
- Validate logical consistency between related configuration options
- Use consistent error message formatting across the codebase

Example of good validation:
```typescript
if (typeof rolloutStep === "number") {
    const allowedSingleValues = [5, 10, 20, 25, 50, 100];
    if (!allowedSingleValues.includes(rolloutStep)) {
        diagnostics.errors.push(
            `"containers.rollout_step_percentage" must be one of [5, 10, 20, 25, 50, 100], but got ${rolloutStep}`
        );
    }
} else if (Array.isArray(rolloutStep)) {
    // Validate array elements and their sum
    const sum = rolloutStep.reduce((acc, step) => acc + step, 0);
    if (sum !== 100) {
        diagnostics.errors.push(
            `"containers.rollout_step_percentage" array elements must sum to 100, but values summed to "${sum}"`
        );
    }
} else {
    diagnostics.errors.push(
        `"containers.rollout_step_percentage" should be an array of numbers or a single number, but got ${JSON.stringify(rolloutStep)}`
    );
}
```

This approach helps users understand exactly what went wrong and how to fix their configuration, reducing support burden and improving developer experience.