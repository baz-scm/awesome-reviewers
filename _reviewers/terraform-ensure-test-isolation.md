---
title: Ensure test isolation
description: "Tests should be completely isolated from each other and clean up after\
  \ themselves to prevent interference. \n\n1. **Use testing utilities properly**:\
  \ Leverage the standard library's testing helpers correctly."
repository: hashicorp/terraform
label: Testing
language: Go
comments_count: 4
repository_stars: 45532
---

Tests should be completely isolated from each other and clean up after themselves to prevent interference. 

1. **Use testing utilities properly**: Leverage the standard library's testing helpers correctly.
   ```go
   // GOOD: Let t.TempDir() handle directory creation and cleanup
   td := t.TempDir()
   
   // BAD: Don't call os.MkdirAll() after t.TempDir()
   td := t.TempDir()
   os.MkdirAll(td, 0755) // Unnecessary - directory already exists with proper permissions
   ```

2. **Clean up global state**: When tests modify global variables or settings, always restore the original values.
   ```go
   // GOOD: Save and restore global state
   p := tfversion.Prerelease
   v := tfversion.Version
   defer func() {
     tfversion.Prerelease = p
     tfversion.Version = v
   }()
   ```

3. **Make tests deterministic**: Avoid non-deterministic behavior like unsorted maps to prevent flaky tests.
   ```go
   // GOOD: Sort keys or values before assertion when using maps
   // Instead of directly asserting on map values which may be in random order
   sortedKeys := make([]string, 0, len(someMap))
   for k := range someMap {
     sortedKeys = append(sortedKeys, k)
   }
   sort.Strings(sortedKeys)
   ```

4. **Validate resource cleanup**: Tests should verify that all resources are properly cleaned up after running.
   ```go
   // Verify no resources remain after test
   if provider.ResourceCount() > 0 {
     t.Fatalf("should have deleted all resources on completion but left %v", 
             provider.ResourceString())
   }
   ```

Properly isolated tests lead to more reliable test suites, easier debugging, and prevent issues where test results depend on execution order.