---
title: standardize log output methods
description: Use `process.stdout.write` instead of `console.log` for controlled logging
  output to avoid linter issues and ensure consistent behavior. When using `process.stdout.write`,
  manually add newlines since they are not automatically appended like with `console.log`.
  Maintain consistent log message formatting with proper prefixes and structured layout.
repository: serverless/serverless
label: Logging
language: JavaScript
comments_count: 4
repository_stars: 46810
---

Use `process.stdout.write` instead of `console.log` for controlled logging output to avoid linter issues and ensure consistent behavior. When using `process.stdout.write`, manually add newlines since they are not automatically appended like with `console.log`. Maintain consistent log message formatting with proper prefixes and structured layout.

Example:
```javascript
// Instead of:
function consoleLog(...args) {
  console.log(...args); // eslint-disable-line no-console
}

// Use:
function writeDeprecation(code, message) {
  process.stdout.write(
    [
      `Serverless: ${chalk.red(`Deprecation Warning: ${message}`)}`,
      `            ${chalk.dim(
        `More Info: https://www.serverless.com/framework/docs/deprecations/#${code}`
      )}`,
    ].join('\n') + '\n'  // Note the explicit newline at the end
  );
}
```

This approach provides better control over output formatting, avoids linter warnings about console usage, and ensures consistent message structure across the application. Always handle edge cases like undefined values in log formatting and maintain proper spacing and alignment in multi-line log messages.