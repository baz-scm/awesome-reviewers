---
title: Write deterministic test assertions
description: 'Tests should be deterministic and explicit in their assertions to ensure
  reliability and maintainability. Follow these guidelines:


  1. Use explicit assertions instead of ambiguous string matching'
repository: docker/compose
label: Testing
language: Go
comments_count: 4
repository_stars: 35858
---

Tests should be deterministic and explicit in their assertions to ensure reliability and maintainability. Follow these guidelines:

1. Use explicit assertions instead of ambiguous string matching
2. Leverage testing utilities provided by the testing framework
3. Test both expected and edge cases
4. Use controlled test data instead of production-like values

Example - Instead of:
```go
assert.Assert(t, strings.Contains(output, "Skipped"))
w.Write([]byte("hello"))
```

Better approach:
```go
// Use explicit assertions
assert.DeepEqual(t, lines, []string{"hello", "world!"})

// Use testing utilities
dirName := t.TempDir()

// Use controlled test data
internal.Version = "v9.9.9-test"

// Test both success and edge cases
w.Write([]byte("hello\n"))
w.Write([]byte("world"))  // Test without EOL
```

This approach makes tests more maintainable, easier to debug, and less prone to flaky failures.