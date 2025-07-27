---
title: avoid hardcoded configuration values
description: Replace hardcoded URLs, ports, file paths, and environment-specific strings
  with configurable parameters. Hardcoded values make code difficult to test, deploy
  across different environments, and maintain over time.
repository: snyk/cli
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 5178
---

Replace hardcoded URLs, ports, file paths, and environment-specific strings with configurable parameters. Hardcoded values make code difficult to test, deploy across different environments, and maintain over time.

Use configuration objects, environment variables, or dependency injection to make values configurable:

```typescript
// Bad: Hardcoded URL
message += `  - ${vulnId} (See https://security.snyk.io/vuln/${vulnId})`;

// Good: Use configuration value
message += `  - ${vulnId} (See ${config.PUBLIC_VULN_DB_URL}/vuln/${vulnId})`;

// Bad: Hardcoded port
const options = new URL(downloadUrl);

// Good: Dynamic port allocation
deepCodeServer = fakeDeepCodeServer();
deepCodeServer.listen(() => {});
env = {
  ...initialEnvVars,
  SNYK_CODE_CLIENT_PROXY_URL: `http://localhost:${deepCodeServer.getPort()}`,
};
```

This approach improves testability by allowing dynamic port allocation, enables environment-specific deployments, and makes the codebase more maintainable. Always prefer configuration injection over hardcoded constants, especially for URLs, API endpoints, file paths, and environment-dependent values.