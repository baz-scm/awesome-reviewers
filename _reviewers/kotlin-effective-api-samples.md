---
title: Effective API samples
description: "Create clear, comprehensive, and properly structured code samples to\
  \ document API usage. Follow these principles:\n\n1. **Organize samples properly:**\n\
  \   - Place samples after doc blocks"
repository: JetBrains/kotlin
label: Documentation
language: Kotlin
comments_count: 8
repository_stars: 50857
---

Create clear, comprehensive, and properly structured code samples to document API usage. Follow these principles:

1. **Organize samples properly:**
   - Place samples after doc blocks
   - For specialized variants, include the main sample first, then add specialized versions:
   ```kotlin
   sample("samples.collections.Collections.Elements.find")
   specialFor(CharSequences) {
       sample("samples.text.Strings.find")
   }
   ```

2. **Create focused examples:**
   - Use separate samples for different overloads of the same function
   - Each sample should clearly demonstrate a specific API feature
   ```kotlin
   @Sample
   fun substring() { // Basic substring usage
       val str = "abcde"
       assertPrints(str.substring(0), "abcde")
       assertPrints(str.substring(1), "bcde")
   }
   
   @Sample
   fun substringWithRange() { // Overload with range
       val str = "abcde"
       assertPrints(str.substring(0, 3), "abc")
       assertPrints(str.substring(0, 0), "")
   }
   ```

3. **Include comprehensive examples:**
   - Demonstrate different parameter combinations
   - Show edge cases and common usage patterns
   - Add explanatory comments for assertions and edge cases
   ```kotlin
   @Sample
   fun lastIndexOf() {
       val inputString = "Never ever give up"
       val toFind = "ever"
       
       // Basic usage from start
       assertPrints(inputString.lastIndexOf(toFind), "6")
       // With specific start position
       assertPrints(inputString.lastIndexOf(toFind, 5), "6")
       // Start position after all occurrences
       assertFails { inputString.lastIndexOf(toFind, 10) } // No occurrence after position 10
   }
   ```

4. **Use standard formatting:**
   - Use `assertPrints()` which converts to readable documentation output
   ```kotlin
   // This:
   assertPrints(value, "stringRepresentation")
   // Converts to:
   println(value) // stringRepresentation
   ```

5. **Ensure samples are properly referenced:**
   - Add `@sample` tags to all relevant function variants, including expect/actual declarations
   - For generated code, update samples by running appropriate generation commands
