---
title: Structure tests thoroughly
description: Create well-structured tests with thorough coverage of both expected
  success and error conditions. Name test cases descriptively to clearly identify
  their purpose, and separate test logic from test data when using table-driven tests.
repository: opentofu/opentofu
label: Testing
language: Go
comments_count: 6
repository_stars: 25901
---

Create well-structured tests with thorough coverage of both expected success and error conditions. Name test cases descriptively to clearly identify their purpose, and separate test logic from test data when using table-driven tests.

**Key practices:**

1. **Use descriptive test case names** to clearly indicate what's being tested:
```go
testCases := map[string]struct {
    name: "should set proxy using http_proxy environment variable",
    rawUrl: "http://example.com",
    httpProxy: "http://foo.bar:3128",
    expectedProxyURL: "http://foo.bar:3128",
}
```
Instead of using unnamed array elements.

2. **Test both success and failure paths** explicitly:
```go
// Ensuring error checks are performed
if tc.wantErr != "" && len(diags) == 0 {
    t.Fatalf("expected error but got none")
}
```

3. **Use proper test resource management** to ensure test isolation:
```go
// Use t.TempDir() instead of manual temp file management
dir := t.TempDir()
// Use t.Helper() in test helpers
t.Helper()
// Use t.Setenv for environment variables
t.Setenv("HTTP_PROXY", tc.httpProxy)
```

4. **Verify both positive and negative expectations** to catch regressions:
```go
// Check for presence of expected value
if !strings.Contains(output, "ami = \"ValueFROMmain/tfvars\"") {
    t.Errorf("expected output to include value from main tfvars")
}
// Check that unwanted value is absent
if strings.Contains(output, "ValueFROMtests/tfvars") {
    t.Errorf("output should not include value from tests tfvars")
}
```

Well-structured tests improve maintainability, make test failures more informative, and provide better protection against regressions.