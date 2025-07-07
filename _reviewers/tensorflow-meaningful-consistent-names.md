---
title: Meaningful consistent names
description: Choose names that are both semantically precise and follow consistent
  conventions. Names should accurately reflect behavior and purpose while adhering
  to established patterns in the codebase.
repository: tensorflow/tensorflow
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 190625
---

Choose names that are both semantically precise and follow consistent conventions. Names should accurately reflect behavior and purpose while adhering to established patterns in the codebase.

**Function naming:**
- Boolean functions should clearly indicate their predicate meaning
  ```cpp
  // Poor: Function returns true for zero values too
  bool IsPositive(const HloInstruction* hlo)
  
  // Better: Name accurately describes behavior
  bool IsNonNegative(const HloInstruction* hlo)
  ```
- If a function extracts or returns more than a boolean, the name should reflect this
  ```cpp
  // Poor: Name suggests it only returns true/false
  bool IsShapedUint8Type(OpBuilder& builder, const Type type, Type& rescaled_type)
  
  // Better: Name indicates it extracts information
  bool ExtractUint8TypeInfo(OpBuilder& builder, const ShapedType type, Type& rescaled_type)
  ```

**Variable naming:**
- Use descriptive names that indicate purpose rather than implementation
  ```cpp
  // Poor: Technical implementation detail
  auto a0_pad_const_op = rewriter.create<tosa::ConstOp>();
  
  // Better: Role-based description
  auto padding_const_op = rewriter.create<tosa::ConstOp>();
  ```
- Prefer full words over abbreviations for clarity
  ```cpp
  // Poor: Abbreviated form
  bool merge_h_to_d_stream = true;
  
  // Better: Fully descriptive
  bool merge_host_to_device_stream = true;
  ```

**Consistency:**
- Follow established casing conventions:
  - Use camelCase for helper functions: `thisIsTheFunctionName()`
  - Use snake_case for variables: `empty_lines` not `emptyLines`
  - Be consistent with compound terms: "LiteRt" not "LiteRT"
- Maintain consistent naming styles within related components to improve API cohesion

These naming practices improve readability, maintainability, and reduce bugs caused by misunderstandings about code behavior.