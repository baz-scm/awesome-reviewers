---
title: Ensure comprehensive test coverage
description: All code paths, error conditions, and edge cases must have corresponding
  unit tests to ensure robust functionality and prevent regressions. This includes
  testing both success and failure scenarios, boundary conditions, and error handling
  paths.
repository: gofiber/fiber
label: Testing
language: Go
comments_count: 9
repository_stars: 37560
---

All code paths, error conditions, and edge cases must have corresponding unit tests to ensure robust functionality and prevent regressions. This includes testing both success and failure scenarios, boundary conditions, and error handling paths.

Key areas requiring test coverage:
- Error handling and validation logic (empty inputs, malformed data, decode failures)
- Edge cases and boundary conditions (negative offsets, missing values, empty collections)
- Both positive and negative test scenarios for configuration flags
- All public functions and methods, especially newly exposed APIs
- Complete coverage of new features and functionality

Example of comprehensive edge case testing:
```go
// Test both positive and negative cases
func Test_Ctx_Subdomains_EdgeCases(t *testing.T) {
    t.Run("negative_offset", func(t *testing.T) {
        c.Request().URI().SetHost("john.doe.google.com")
        require.Empty(t, c.Subdomains(-1), "negative offset should return empty slice")
    })
    
    t.Run("offset_too_high", func(t *testing.T) {
        c.Request().URI().SetHost("john.doe.is.awesome.google.com")
        require.Empty(t, c.Subdomains(10))
    })
}

// Test error handling paths
func Test_parseAndClearFlashMessages_DecodeError(t *testing.T) {
    // Test when hex.DecodeString fails
    cookieValue, err := hex.DecodeString(invalidHexString)
    if err != nil {
        // Verify that no flash messages are processed
        require.Len(t, r.c.flashMessages, 0, "Expected no flash messages when decode fails")
    }
}
```

Missing test coverage often indicates incomplete validation of functionality and can lead to production bugs. Use code coverage tools to identify untested paths and ensure critical error handling is properly validated.