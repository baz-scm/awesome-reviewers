---
title: Use table-driven tests
description: In Go, prefer table-driven tests over multiple separate test functions.
  Table tests allow for concise testing of multiple scenarios, improve code readability,
  and make it easier to add new test cases.
repository: kubeflow/kubeflow
label: Testing
language: Go
comments_count: 3
repository_stars: 15064
---

In Go, prefer table-driven tests over multiple separate test functions. Table tests allow for concise testing of multiple scenarios, improve code readability, and make it easier to add new test cases.

A table-driven test consists of:
1. A slice of test cases, each containing input and expected output
2. A loop that executes the same test logic for each case
3. Clear error messages that identify which test case failed

Example:
```go
func TestSomething(t *testing.T) {
    tests := []struct {
        name     string
        input    map[string]string
        expected map[string]string
    }{
        {
            name:     "case1",
            input:    map[string]string{"key1": "value1"},
            expected: map[string]string{"key1": "value1", "defaultKey": "defaultValue"},
        },
        {
            name:     "case2",
            input:    map[string]string{},
            expected: map[string]string{"defaultKey": "defaultValue"},
        },
    }
    
    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            result := functionUnderTest(test.input)
            if !reflect.DeepEqual(result, test.expected) {
                t.Errorf("Expected:\n%v\nGot:\n%v", test.expected, result)
            }
        })
    }
}
```

This pattern makes your test suite more maintainable and encourages thorough testing of edge cases by making it trivial to add new scenarios. When reviewing code, ensure new functionality is tested with table-driven tests rather than creating separate test functions for related scenarios.
