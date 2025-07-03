---
title: Follow Swift conventions
description: 'When designing and documenting APIs in Swift, adhere to Swift''s established
  naming conventions and documentation practices:


  1. **Use correct initializer syntax**: Swift initializers should not form phrases
  with argument labels. Avoid prepositions in argument labels.'
repository: tensorflow/swift
label: API
language: Markdown
comments_count: 2
repository_stars: 6136
---

When designing and documenting APIs in Swift, adhere to Swift's established naming conventions and documentation practices:

1. **Use correct initializer syntax**: Swift initializers should not form phrases with argument labels. Avoid prepositions in argument labels.

   ```swift
   // Incorrect
   let tensor = Tensor(fromNumpyArray: array)
   
   // Correct
   let tensor = Tensor(numpy: array)
   ```

2. **Document APIs completely**: When referencing APIs in documentation, include both the original framework name and the complete Swift method signature with parameter names.

   ```
   // Incomplete
   The saveV2 and restoreV2 ops are now supported.
   
   // Complete
   `SaveV2` (`Raw.saveV2(prefix:tensorNames:shapeAndSlices:tensors:)`), `RestoreV2` (`Raw.restoreV2(prefix:tensorNames:shapeAndSlices:dtypes:)`)
   ```

3. **Use official terminology**: Maintain consistent terminology across documentation and code (e.g., use "operator" instead of "op").

4. **Add API links**: Where possible, include links to API documentation to enhance discoverability and understanding.

These practices ensure that your APIs are consistent with Swift ecosystem standards, making them more intuitive and discoverable for developers.
