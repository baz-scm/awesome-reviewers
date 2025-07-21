---
title: Specific assertion methods
description: Use the most specific and descriptive assertion methods available in
  your test framework to improve test readability and failure diagnostics. Prefer
  methods that clearly state intent and produce helpful error messages.
repository: temporalio/temporal
label: Testing
language: Go
comments_count: 6
repository_stars: 14953
---

Use the most specific and descriptive assertion methods available in your test framework to improve test readability and failure diagnostics. Prefer methods that clearly state intent and produce helpful error messages.

Examples:
- Use `require.Empty(t, collection)` instead of `require.Len(t, collection, 0)`
- Use `require.NotZero(t, count)` instead of `require.True(t, count > 0)`
- Use `assert.EqualExportedValues(t, expected, actual)` instead of `proto.Equal()` to get helpful diffs on failure
- Use table-driven tests to test similar functionality with different inputs:

```go
func TestCollectionAttributes(t *testing.T) {
    // Define test cases for both string and int keys
    testCases := []struct{
        name string
        keyType string
        expected interface{}
    }{
        {"StringKey", "string", expectedStringResult},
        {"IntKey", "int", expectedIntResult},
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            // Test logic with tc.keyType and tc.expected
        })
    }
}
```

Also use descriptive test names that follow a pattern like `TestComponent_Behavior_Condition` (e.g., `TestLogger_FilesArentRotated_WhenDisabled`) to clearly communicate what's being tested.

These practices make tests more maintainable, easier to debug when they fail, and the intent clearer to other developers.