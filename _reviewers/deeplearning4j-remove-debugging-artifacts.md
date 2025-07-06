---
title: Remove debugging artifacts
description: Production code should be free from debugging artifacts that reduce readability
  and maintainability. Remove all debugging print statements, commented-out code blocks,
  and other temporary debugging elements before merging code.
repository: deeplearning4j/deeplearning4j
label: Code Style
language: C++
comments_count: 9
repository_stars: 14036
---

Production code should be free from debugging artifacts that reduce readability and maintainability. Remove all debugging print statements, commented-out code blocks, and other temporary debugging elements before merging code.

Specifically:

1. **Remove all debugging print statements**:
   Debug prints should only appear in development branches or be wrapped in appropriate debug-only conditions.

   ```cpp
   // BAD: Unconditional debug printing
   sd_printf("Before op execution \n", 0);
   
   // GOOD: Conditional printing only when needed
   if (LOG_LEVEL >= DEBUG) {
       sd_printf("Before op execution \n", 0);
   }
   ```

2. **Delete commented-out code**:
   Commented-out code creates confusion about which implementation is correct and clutters the codebase.

   ```cpp
   // BAD: Leaving commented-out code without explanation
   //REQUIRE_TRUE(expectedUpdShape == updShape, 0, "SCATTER_ADD OP: wrong shape of updates array...");
   
   // GOOD: Either remove it entirely or provide a clear justification comment
   // REQUIRE statement intentionally disabled during beta testing until shape validation is fixed in issue #1234
   //REQUIRE_TRUE(expectedUpdShape == updShape, 0, "SCATTER_ADD OP: wrong shape of updates array...");
   ```

3. **Clean up unused variables and redundant operations**:
   Remove variables that are declared but never used.

If debugging functionality needs to be preserved for future troubleshooting, consider implementing proper logging with configurable levels rather than leaving print statements scattered throughout the code.