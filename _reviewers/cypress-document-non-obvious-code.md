---
title: Document non-obvious code
description: Add explanatory comments when code logic is unclear, implements workarounds,
  or has special reasoning that isn't immediately apparent to other developers. Comments
  should explain the "why" behind the implementation, not just the "what".
repository: cypress-io/cypress
label: Documentation
language: JavaScript
comments_count: 2
repository_stars: 48850
---

Add explanatory comments when code logic is unclear, implements workarounds, or has special reasoning that isn't immediately apparent to other developers. Comments should explain the "why" behind the implementation, not just the "what".

This includes:
- Documenting the rationale behind hacks or workarounds
- Explaining complex or non-intuitive logic flows  
- Providing context for special cases or edge case handling
- Linking to relevant issues or documentation when applicable

Example:
```javascript
// Fetch a dynamic import and re-try 3 times with a 2-second back-off
// See GitHub issue #1234 - this works around intermittent module loading failures
function retryImport(modulePath) {
  // implementation here
}

onStudioTestFileChange(filePath) {
  // wait for the studio test file to be written to disk, then reload the test
  return this.onTestFileChange(filePath).then(() => {
    // rest of implementation
  })
}
```

The goal is to make code self-documenting and reduce the cognitive load for future maintainers who need to understand the reasoning behind implementation decisions.