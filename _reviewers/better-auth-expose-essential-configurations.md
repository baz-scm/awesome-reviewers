---
title: Expose essential configurations
description: Carefully evaluate which configuration options should be exposed to users
  versus kept internal. Not all configuration parameters need to be user-controllable
  - expose only those that provide meaningful customization while keeping implementation
  details private.
repository: better-auth/better-auth
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 19651
---

Carefully evaluate which configuration options should be exposed to users versus kept internal. Not all configuration parameters need to be user-controllable - expose only those that provide meaningful customization while keeping implementation details private.

For user-facing configurations, provide multiple access methods appropriate to the use case:
- Environment variables for deployment-specific settings
- Plugin/library options for functional customization  
- Avoid CLI-only configuration for library features

Consider the deployment context when designing configuration storage. For libraries that may run in serverless environments, avoid persistent global configuration files that won't work across ephemeral instances.

Example of appropriate configuration exposure:
```typescript
// Good: Essential user configurations exposed
interface DeviceAuthorizationOptions {
  expiresIn?: number;           // User should control
  interval?: number;            // User should control  
  verificationUri?: string;     // User should control
}

// Good: Internal implementation details not exposed
const opts = {
  deviceCodeLength: 40,         // Internal default
  enableRateLimiting: true,     // Internal behavior
  ...options,                   // User overrides
};

// Avoid: Exposing internal endpoints
telemetry?: {
  endpoint?: string;  // Internal implementation detail
}
```

Provide environment variable alternatives for settings that affect behavior across projects, allowing users to disable or configure features globally when appropriate.