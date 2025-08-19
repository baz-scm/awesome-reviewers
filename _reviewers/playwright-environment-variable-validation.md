---
title: Environment variable validation
description: Environment variables should be properly validated, parsed, and have
  sensible fallback values. Always validate boolean environment variables using explicit
  string comparisons rather than truthy checks, provide clear default values, and
  implement proper error handling for malformed values.
repository: microsoft/playwright
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 76113
---

Environment variables should be properly validated, parsed, and have sensible fallback values. Always validate boolean environment variables using explicit string comparisons rather than truthy checks, provide clear default values, and implement proper error handling for malformed values.

Key practices:
- Use explicit string comparisons for boolean environment variables: `process.env.VAR === '1' || process.env.VAR === 'true'`
- Provide meaningful defaults when environment variables are missing or invalid
- Support multiple formats when appropriate (e.g., `PLAYWRIGHT_FORCE_TTY` supporting boolean, width, or "widthxheight" formats)
- Use environment variables as feature gates for platform-specific or experimental functionality
- Validate and sanitize environment variable values before use

Example:
```typescript
// Good: Explicit validation with defaults
const headless = process.env.PLAYWRIGHT_HEADLESS === '1' || process.env.PLAYWRIGHT_HEADLESS === 'true';
const allowAndroid = process.env.PLAYWRIGHT_ALLOW_ANDROID === '1';

// Good: Complex parsing with fallbacks
const sizeMatch = process.env.PLAYWRIGHT_FORCE_TTY?.match(/^(\d+)x(\d+)$/);
if (sizeMatch) {
  ttyWidth = +sizeMatch[1];
  ttyHeight = +sizeMatch[2];
} else {
  ttyWidth = +process.env.PLAYWRIGHT_FORCE_TTY || DEFAULT_TTY_WIDTH;
}

// Bad: Truthy check without explicit validation
if (process.env.SOME_FLAG) { /* unreliable */ }
```

This prevents configuration bugs, improves security by requiring explicit opt-ins for sensitive features, and ensures consistent behavior across different environments.