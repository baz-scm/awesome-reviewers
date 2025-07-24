---
title: Extract testable units
description: Avoid copying or reimplementing production logic in test files. Instead,
  refactor the production code to extract small, testable functions that can be unit
  tested with mocked dependencies. Tests should call the actual production functions
  rather than duplicating their logic.
repository: argoproj/argo-cd
label: Testing
language: Go
comments_count: 3
repository_stars: 20149
---

Avoid copying or reimplementing production logic in test files. Instead, refactor the production code to extract small, testable functions that can be unit tested with mocked dependencies. Tests should call the actual production functions rather than duplicating their logic.

When you find yourself copying complex logic from production code into tests, this indicates the production code needs refactoring. Extract the core logic into smaller, focused functions that accept dependencies as parameters, making them easier to test in isolation.

For example, instead of reimplementing import logic in a test:
```go
// Bad: Reimplementing logic in test
func Test_importResources(t *testing.T) {
    // ... lots of copied logic from backup.go
    if bakObj.GetKind() == "Secret" {
        dynClient = dynamicClient.Resource(secretResource).Namespace(bakObj.GetNamespace())
    }
    // ... more copied logic
}

// Good: Extract testable function and test it
func (opts *importOpts) executeImport(client dynamic.Interface) error {
    // extracted logic here
}

func Test_executeImport(t *testing.T) {
    fakeClient := dynamicfake.NewSimpleDynamicClient(scheme)
    opts := &importOpts{...}
    err := opts.executeImport(fakeClient)
    // verify results by querying the fake client
}
```

This approach creates more maintainable tests, reduces code duplication, and ensures tests actually validate the production code rather than a separate implementation.