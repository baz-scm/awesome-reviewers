---
title: debug logging reliability
description: Ensure debug logging behaves correctly by only activating when debug
  flags are explicitly enabled, while providing comprehensive coverage of all relevant
  cases when active. Debug logs should not cause application failures and should be
  printed for all error conditions, not just specific subsets.
repository: snyk/cli
label: Logging
language: TypeScript
comments_count: 4
repository_stars: 5178
---

Ensure debug logging behaves correctly by only activating when debug flags are explicitly enabled, while providing comprehensive coverage of all relevant cases when active. Debug logs should not cause application failures and should be printed for all error conditions, not just specific subsets.

Key principles:
- Debug logs should only appear when debug mode is explicitly enabled (e.g., `-d` flag)
- When enabled, debug logs should cover all relevant cases, including errors that don't appear in main error reporting
- Logging errors should never cause the main functionality to fail early
- Test debug logging functionality to ensure it works as expected

Example of proper debug setup:
```typescript
// Correct: Debug only enabled when intended
const debug = debugLib('snyk-code');

// Incorrect: Always enabling debug
debugLib.enable('snyk-code');
const debug = debugLib('snyk-code');
```

Example of comprehensive debug coverage:
```typescript
// Print debug logs for all cases, not just specific conditions
if (debugLogs[fileData.filePath]) {
  debug(
    'File %s failed to parse with: %s',
    fileData.filePath,
    debugLogs[fileData.filePath],
  );
}
```