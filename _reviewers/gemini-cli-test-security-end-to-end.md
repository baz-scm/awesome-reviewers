---
title: test security end-to-end
description: Security features must be tested using the actual executable or CLI rather
  than just module-level unit tests. This ensures the complete security mechanism
  works end-to-end in the real execution environment, not just individual components
  in isolation.
repository: google-gemini/gemini-cli
label: Security
language: JavaScript
comments_count: 1
repository_stars: 65062
---

Security features must be tested using the actual executable or CLI rather than just module-level unit tests. This ensures the complete security mechanism works end-to-end in the real execution environment, not just individual components in isolation.

When implementing security controls like environment variable isolation, input validation, or authentication flows, create integration tests that invoke the actual product executable to validate the security behavior works as intended from the user's perspective.

Example:
```javascript
// Good: Test security feature with actual CLI
const output = execSync(
  `node packages/cli/index.js --ignore-local-env`,
  { cwd: testProjectDir, encoding: 'utf8' }
);
// Verify malicious .env files are NOT loaded

// Avoid: Only testing the security logic in isolation
const result = envLoader.loadWithIsolation(options);
```

This approach catches security vulnerabilities that might only manifest when all components work together, such as configuration precedence issues, CLI argument parsing bugs, or execution context problems that could bypass security controls.