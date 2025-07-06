---
title: Clean up your code
description: "Maintain clean, professional code by removing development artifacts\
  \ and improving readability:\n\n1. **Remove debug code before committing**:\n  \
  \ - Delete all debugging print statements"
repository: deeplearning4j/deeplearning4j
label: Code Style
language: Java
comments_count: 13
repository_stars: 14036
---

Maintain clean, professional code by removing development artifacts and improving readability:

1. **Remove debug code before committing**:
   - Delete all debugging print statements
   - Remove commented-out code blocks
   - If keeping temporarily disabled code is necessary, add a clear TODO comment

   ```java
   // Bad:
   System.out.println("Functrace on: " + funcTrace);
   
   // Bad:
   // ptrDataBuffer.closeBuffer();
   // if(pointer != null && !pointer.isNull())
   //     pointer.close();
   
   // If really necessary:
   // TODO: Re-enable this after fixing JIRA-1234
   // ptrDataBuffer.closeBuffer();
   ```

2. **Replace magic numbers with named constants**:
   - Extract hard-coded numeric literals into meaningful constants
   - Place constants at the class level for reuse and clarity

   ```java
   // Bad:
   if (edgeCount - lastEdgeCount > 10000) {
     // ...
   }
   
   // Good:
   private static final int EDGE_COUNT_REPORT_THRESHOLD = 10000;
   
   if (edgeCount - lastEdgeCount > EDGE_COUNT_REPORT_THRESHOLD) {
     // ...
   }
   ```

3. **Format precondition checks properly**:
   - Use string formatting instead of concatenation to avoid unnecessary object creation
   - Include the actual values in the error message for easier debugging

   ```java
   // Bad:
   Preconditions.checkArgument(data >= 0,
           "Values for " + paramName + " must be >= 0, got: " + data);
   
   // Good:
   Preconditions.checkArgument(data >= 0, "Values for %s must be >= 0, got %s", paramName, data);
   ```

4. **Add private constructors to utility classes**:
   - Prevent instantiation of utility classes with private constructors

   ```java
   // Good:
   public class ValidationUtils {
       private ValidationUtils() {
           // Private constructor to prevent instantiation
       }
       
       // Static utility methods...
   }
   ```