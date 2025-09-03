---
title: Update deprecated demo APIs
description: Documentation, demos, and example code should always use current, non-deprecated
  APIs instead of showing deprecation warnings. When APIs are deprecated, update all
  demo code and examples to use the recommended replacement APIs immediately.
repository: ant-design/ant-design
label: API
language: Other
comments_count: 4
repository_stars: 95882
---

Documentation, demos, and example code should always use current, non-deprecated APIs instead of showing deprecation warnings. When APIs are deprecated, update all demo code and examples to use the recommended replacement APIs immediately.

This prevents users from copying outdated code that generates warnings and ensures documentation serves as a reliable guide for current best practices. If deprecated API compatibility testing is needed, limit it to dedicated test files rather than user-facing examples.

Example of what to avoid:
```typescript
// Bad: Demo showing deprecated API usage
<Alert onClose={handleClose} /> // Generates warning

// Good: Demo using current API
<Alert closable={{ onClose: handleClose }} />
```

When you see deprecation warnings in demo snapshots, update the demo source code to use the current API rather than accepting the warning as expected output.