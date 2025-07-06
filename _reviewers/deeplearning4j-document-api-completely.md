---
title: Document API completely
description: 'All public APIs must have comprehensive and clear documentation that
  helps developers understand functionality without examining implementation details.
  Follow these guidelines:'
repository: deeplearning4j/deeplearning4j
label: Documentation
language: Java
comments_count: 8
repository_stars: 14036
---

All public APIs must have comprehensive and clear documentation that helps developers understand functionality without examining implementation details. Follow these guidelines:

1. **Methods and classes**: Document the purpose, behavior, parameters, and return values. Class-level documentation should explain usage patterns and limitations.
   ```java
   /**
    * Standardize input variable along given axis by subtracting mean and dividing by standard deviation.
    * 
    * @param input The input variable to standardize
    * @param dimensions Dimensions along which to calculate statistics
    * @return Standardized variable with zero mean and unit variance along specified dimensions
    */
   public SDVariable standardize(SDVariable input, int... dimensions) {
       // Implementation
   }
   ```

2. **Empty or non-obvious implementations**: Always include comments explaining why a method is empty or has unexpected behavior.
   ```java
   @Override
   public void setValue(Number value) {
       // No action needed - this method intentionally left empty as value is managed by parent condition
   }
   ```

3. **Deprecation**: Follow this format for all deprecated elements:
   - Add `@Deprecated` annotation
   - Include `@deprecated` Javadoc tag explaining why and what to use instead
   - Use `{@link}` references to replacements
   ```java
   /**
    * @deprecated As of version 1.0.0-beta, replaced by {@link #newMethod()} which provides better performance
    */
   @Deprecated
   public void oldMethod() {
       // Implementation
   }
   ```

4. **Method references**: Ensure `@see` and `{@link}` references are accurate and helpful. For overloaded methods, clearly specify which signature is being referenced and explain default behavior.
   ```java
   /**
    * As per {@link #pad(INDArray, int[][], List<double[]>, PadMode)} with 'constantValues' being zeros (zero padding)
    */
   public static INDArray pad(INDArray toPad, int[][] padWidth, PadMode padMode) {
       // Implementation
   }
   ```

5. **Special elements**: Document enum values appropriately with Javadoc rather than inline comments.
   ```java
   public enum WeightsFormat {
       /**
        * Kernel height, kernel width, input channels, output channels [kH, kW, iC, oC]
        */
       YXIO,
       
       /**
        * Output channels, input channels, kernel height, kernel width [oC, iC, kH, kW]
        */
       OIYX
   }
   ```