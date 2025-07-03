---
title: Robust test assertions
description: Use precise, informative assertions in tests to provide clear feedback
  when tests fail and verify the correct behavior rather than implementation details.
repository: elastic/elasticsearch
label: Testing
language: Java
comments_count: 6
repository_stars: 73104
---

Use precise, informative assertions in tests to provide clear feedback when tests fail and verify the correct behavior rather than implementation details.

**Key practices:**

1. **Use assertion methods with descriptive messages**: Replace plain `assert` statements with proper test framework assertions that provide clear error messages.
   ```java
   // Instead of this:
   assert valueCount == 1;
   
   // Do this:
   assertEquals(1, valueCount, "Multi-values make chunking more complex, and it's not a real case yet");
   ```

2. **Use expectThrows for exception testing**: Replace try-catch blocks with more readable and concise expectThrows pattern.
   ```java
   // Instead of this:
   try {
       createComponents("my_analyzer", analyzerSettings, testAnalysis.tokenizer, testAnalysis.charFilter, testAnalysis.tokenFilter);
       fail("expected failure");
   } catch (IllegalArgumentException e) {
       // assertions
   }
   
   // Do this:
   IllegalArgumentException e = expectThrows(
       IllegalArgumentException.class,
       () -> createComponents("my_analyzer", analyzerSettings, testAnalysis.tokenizer, testAnalysis.charFilter, testAnalysis.tokenFilter)
   );
   // assertions on exception
   ```

3. **Focus assertions on behavior, not implementation details**: Verify that the code does the right thing, not how it does it.
   ```java
   // Instead of verifying exact implementation details:
   verify(coordinatingIndexingPressure).increment(1, bytesUsed(doc0Source));
   verify(coordinatingIndexingPressure).increment(1, bytesUsed(doc1Source));
   
   // Verify the essential behavior:
   verify(coordinatingIndexingPressure, times(6)).increment(eq(1), longThat(l -> l > 0));
   ```

4. **Verify all relevant fields**: Assert on all important aspects of the test output, not just a subset.

5. **Randomize test values**: Use randomized values instead of hardcoded constants to ensure tests catch edge cases.
   ```java
   // Instead of hardcoded values:
   String apiKeyId = "test-id";
   
   // Use randomization:
   String apiKeyId = randomAlphaOfLength(20);
   ```

6. **Use appropriate matchers**: For values that may vary, use flexible assertions like `greaterThanOrEqualTo()` instead of strict equality.
