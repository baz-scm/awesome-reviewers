---
title: Use appropriate testify assertions
description: Choose the most specific and appropriate testify assertion methods for
  your test scenarios to improve test clarity, error reporting, and maintainability.
repository: gravitational/teleport
label: Testing
language: Go
comments_count: 5
repository_stars: 19109
---

Choose the most specific and appropriate testify assertion methods for your test scenarios to improve test clarity, error reporting, and maintainability.

Key guidelines:

1. **Use `require` in `EventuallyWithT` functions**: As of testify v1.10.0, `require` can be used within `EventuallyWithT` and will cause early return on failure, triggering a retry on the next tick.

```go
require.EventuallyWithT(t, func(t *assert.CollectT) {
    trackers, err := auth.GetActiveSessionTrackers(ctx)
    require.NoError(t, err)  // Use require, not assert
    require.Len(t, trackers, 1)
    require.Equal(t, helpers.HostID, trackers[0].GetAddress())
})
```

2. **Use specialized error assertion methods**: Instead of combining generic assertions, use specific methods like `require.ErrorContains` for error message validation.

```go
// Instead of:
require.Error(t, err)
require.Contains(t, err.Error(), tt.errMsg)

// Use:
require.ErrorContains(t, err, tt.errMsg)
```

3. **Use structured data assertions**: For JSON and YAML comparisons, use semantic equality assertions rather than string matching.

```go
// Instead of string comparison:
require.Contains(t, captureStdout.String(), tc.wantOutput())

// Use semantic comparison:
require.JSONEq(t, expectedJSON, actualJSON)
require.YAMLEq(t, expectedYAML, actualYAML)
```

These specialized assertions provide better error messages, handle formatting differences, and make test intentions clearer to other developers.