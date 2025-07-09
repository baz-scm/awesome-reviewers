---
title: Use testify assertion libraries
description: Replace manual if-error checks with `testify`'s `assert` and `require`
  packages to make tests more readable, maintainable, and with better error messages.
repository: vitessio/vitess
label: Testing
language: Go
comments_count: 12
repository_stars: 19815
---

Replace manual if-error checks with `testify`'s `assert` and `require` packages to make tests more readable, maintainable, and with better error messages.

**When to use each:**
- Use `assert` for non-critical checks that should report failures but continue testing
- Use `require` for checks that should halt the test if they fail

**Key improvements:**

1. **Replace manual comparisons with appropriate assertions**
```go
// Before
if !ok || v != data {
    t.Errorf("Cache has incorrect value: %v != %v", data, v)
}

// After
assert.True(t, ok, "Value should be found in cache")
assert.Equal(t, data, v, "Cache should return correct value")
```

2. **Split compound conditions into separate assertions**
```go
// Before
if !triggered1 || !triggered2 {
    t.Errorf("not all matching listeners triggered")
}

// After
assert.True(t, triggered1, "First listener should be triggered")
assert.True(t, triggered2, "Second listener should be triggered")
```

3. **Use type-compatible assertions to avoid unnecessary casting**
```go
// Before
if got := int(h.Records()[0].(mod10)); got != 1 {
    t.Errorf("h.Records()[0] = %v, want %v", got, 1)
}

// After
assert.EqualValues(t, 1, h.Records()[0].(mod10))
```

4. **Use specialized assertions for common operations**
```go
// Before
if len(values) != 1 {
    t.Errorf("Expected exactly one value, got %d", len(values))
}

// After
require.Len(t, values, 1, "Should have exactly one value")
```

5. **Use appropriate error validation**
```go
// Before
if err == nil {
    t.Fatalf("Expected error but got none")
}

// After
require.Error(t, err, "Operation should return an error")
// Or to check specific error text
require.ErrorContains(t, err, "expected error message")
```

Using these assertion functions consistently improves readability, provides better error messages, and makes tests more maintainable.