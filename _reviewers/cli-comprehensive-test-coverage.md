---
title: comprehensive test coverage
description: Ensure thorough test coverage by extracting complex logic into small,
  testable functions and using appropriate testing utilities. When encountering complex
  code blocks, break them into smaller functions that can be tested in isolation.
  Use Go's built-in testing utilities like `t.Setenv()` instead of `os.Setenv()` for
  environment variables, and...
repository: snyk/cli
label: Testing
language: Go
comments_count: 5
repository_stars: 5178
---

Ensure thorough test coverage by extracting complex logic into small, testable functions and using appropriate testing utilities. When encountering complex code blocks, break them into smaller functions that can be tested in isolation. Use Go's built-in testing utilities like `t.Setenv()` instead of `os.Setenv()` for environment variables, and `assert.Eventually()` instead of `time.Sleep()` for timing-dependent assertions. Cover multiple scenarios in your tests, including edge cases and different input conditions.

Example of extracting testable logic:
```go
// Instead of testing complex inline logic
func (c *CLI) getErrorFromFile(errFilePath string) (data error, err error) {
    // ... complex logic here
    if len(jsonErrors) != 0 {
        useSTDIO := c.globalConfig.GetBool(configuration.WORKFLOW_USE_STDIO)
        // more complex processing...
    }
}

// Extract into testable function
func shouldUseSTDIO(config Config, jsonErrors []Error) bool {
    if len(jsonErrors) != 0 {
        return config.GetBool(configuration.WORKFLOW_USE_STDIO)
    }
    return false
}

// Test the extracted function
func Test_shouldUseSTDIO(t *testing.T) {
    t.Run("with errors", func(t *testing.T) {
        // test logic here
    })
    t.Run("without errors", func(t *testing.T) {
        // test logic here  
    })
}
```

Use proper testing utilities:
```go
// Prefer this
func TestWithEnv(t *testing.T) {
    t.Setenv("SNYK_TOKEN", "invalidToken")
    // test logic
}

// Over this
func TestWithEnv(t *testing.T) {
    os.Setenv("SNYK_TOKEN", "invalidToken")
    defer os.Unsetenv("SNYK_TOKEN")
    // test logic
}
```