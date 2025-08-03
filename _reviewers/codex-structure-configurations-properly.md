---
title: Structure configurations properly
description: Define a clear, hierarchical structure for application configurations
  with descriptive naming and proper organization. Avoid hardcoded values, use named
  constants for magic numbers, and ensure configuration is loaded only once at startup
  and passed through the application rather than loaded at arbitrary points.
repository: openai/codex
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 31275
---

Define a clear, hierarchical structure for application configurations with descriptive naming and proper organization. Avoid hardcoded values, use named constants for magic numbers, and ensure configuration is loaded only once at startup and passed through the application rather than loaded at arbitrary points.

**Key practices:**

1. **Use named constants instead of magic values:**
   ```typescript
   // Avoid
   const deadline = Date.now() + 1000;
   
   // Better
   const PROCESS_TERMINATION_TIMEOUT_MS = 1000;
   const deadline = Date.now() + PROCESS_TERMINATION_TIMEOUT_MS;
   ```

2. **Organize configurations hierarchically by functionality:**
   ```typescript
   // Avoid
   output: {
     maxBytes: 12410,
     maxLines: 256
   }
   
   // Better
   tools: {
     shell: {
       maxBytes: 12410,
       maxLines: 256
     }
   }
   ```

3. **Externalize hardcoded values:**
   ```typescript
   // Avoid
   client_id: "Iv1.b507a08c87ecfe98"
   
   // Better
   client_id: process.env.GITHUB_CLIENT_ID || config.github.clientId
   ```

4. **Load configuration once and thread it through:**
   ```typescript
   // Avoid
   function someFunction() {
     const config = loadConfig(); // Loading config at arbitrary points
     // ...
   }
   
   // Better
   function someFunction(config) { // Config passed as parameter
     // ...
   }
   ```

5. **Provide sensible defaults when configuration is missing:**
   ```typescript
   // Avoid
   const providersConfig = config.providers; // Could be undefined
   
   // Better
   const providersConfig = config.providers ?? defaultProviders;
   ```

Following these practices makes configurations more maintainable, testable, and prevents unpredictable behavior in long-running applications when configurations change during execution.