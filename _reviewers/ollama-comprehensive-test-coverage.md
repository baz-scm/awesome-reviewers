---
title: Comprehensive test coverage
description: 'Test functions should provide comprehensive coverage of both expected
  and edge cases. Include tests for:


  1. **Boundary conditions**: Test zero, minimum, maximum values, and other special
  cases.'
repository: ollama/ollama
label: Testing
language: Go
comments_count: 5
repository_stars: 145704
---

Test functions should provide comprehensive coverage of both expected and edge cases. Include tests for:

1. **Boundary conditions**: Test zero, minimum, maximum values, and other special cases.
   ```go
   func TestTemperature(t *testing.T) {
     // Test normal case
     logits, err := Temperature(0.5).Apply([]float64{-3, -2, -1, 0, 1, 2, 4})
     if err != nil {
       t.Error(err)
     }
     
     // Test boundary case (zero)
     logits, err = Temperature(0).Apply([]float64{-3, -2, -1, 0, 1, 2, 4})
     if err != nil {
       t.Error(err)
     }
   }
   ```

2. **Varied input patterns**: Test unsorted, sorted, empty, and different input formats.
   ```go
   // Test with unsorted inputs
   logits, err := Temperature(0.5).Apply([]float64{2, -1, 4, -3, 1, -2, 0})
   ```

3. **Multiple levels of granularity**: Test intermediate steps as well as end-to-end functionality.
   ```go
   // Don't just test ParseToolCalls, but also intermediate steps
   func TestFindTemplatePrefix(t *testing.T) { /* ... */ }
   func TestExtractToolTokens(t *testing.T) { /* ... */ }
   func TestParseToolCalls(t *testing.T) { /* ... */ }
   ```

4. **Both valid and invalid cases**: Each test function should validate both expected successful cases and error conditions.
   ```go
   tests := []struct {
     name    string
     input   string
     valid   bool
     want    Result
     wantErr error
   }{
     {
       name:  "valid input",
       input: "valid data",
       valid: true,
       want:  expectedResult,
     },
     {
       name:    "invalid input",
       input:   "invalid data",
       valid:   false,
       wantErr: ErrInvalidData,
     },
   }
   ```

Thorough test coverage helps catch edge cases and ensures code robustness, particularly for functionality that may be used across different parts of the system.