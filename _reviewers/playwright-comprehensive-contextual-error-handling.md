---
title: Comprehensive contextual error handling
description: Implement thorough error handling that goes beyond basic logging and
  provides contextually accurate, actionable error messages. Error handling should
  include proper propagation, recovery mechanisms where appropriate, and messages
  that reflect the actual system state and available options.
repository: microsoft/playwright
label: Error Handling
language: Other
comments_count: 2
repository_stars: 76113
---

Implement thorough error handling that goes beyond basic logging and provides contextually accurate, actionable error messages. Error handling should include proper propagation, recovery mechanisms where appropriate, and messages that reflect the actual system state and available options.

Avoid minimal error handling that only logs errors:
```javascript
// Inadequate - just logs and continues
socket.on('error', (error) => console.log('socket error from wrapper', error));
```

Instead, implement comprehensive error handling with context-aware messaging:
```javascript
// Better - proper error handling with context
socket.on('error', (error) => {
    console.error('Socket connection failed:', error.message);
    process.exit(1); // or appropriate recovery mechanism
});

// Context-aware error messages
if (!(await fs.promises.stat(executable)).isFile()) {
    const packageManager = detectPackageManager(); // Use actual detected manager
    throw new Error(`Executable does not exist. Did you update Playwright recently? Make sure to run ${packageManager} playwright install webkit-wsl`);
}
```

Error messages should be accurate to the current system context and provide specific, actionable guidance rather than generic assumptions about user environment or tooling.