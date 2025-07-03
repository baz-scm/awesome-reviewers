---
title: Maintainable test structure
description: 'Write tests that are maintainable, self-documenting, and that promote
  good testing practices:


  1. **Use proper assertion mechanisms**: Prefer modern assertion patterns over legacy
  approaches. Use built-in assertion methods that clearly indicate what is being tested.'
repository: dotnet/runtime
label: Testing
language: C#
comments_count: 5
repository_stars: 16578
---

Write tests that are maintainable, self-documenting, and that promote good testing practices:

1. **Use proper assertion mechanisms**: Prefer modern assertion patterns over legacy approaches. Use built-in assertion methods that clearly indicate what is being tested.
   ```csharp
   // Bad: Custom test logic with manual exception checking
   bool canceled = false;
   try {
       await GetAsync(useVersion, testAsync, uri, cts.Token);
   } catch (TaskCanceledException) {
       canceled = true;
   }
   Assert.True(canceled);
   
   // Good: Use built-in assertion methods
   await Assert.ThrowsAsync<TaskCanceledException>(() => 
       GetAsync(useVersion, testAsync, uri, cts.Token));
   ```

2. **Create reusable test helpers** for common operations instead of duplicating test code. This improves maintainability and readability while reducing the chance of inconsistencies.

3. **Use modern test patterns**: Replace legacy patterns like "return 100 == success" with proper Assert-based validation that clearly communicates test expectations and failures.

4. **Remove commented-out or dead test code** that doesn't contribute to validation. Keep tests clean and focused on what's actually being tested.

5. **Use appropriate conditional attributes** to ensure tests properly convert Debug.Assert failures to test failures and run only when the tested functionality is supported.
