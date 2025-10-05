---
title: Improve code readability
description: 'Enhance code clarity and maintainability by applying several readability
  techniques: extract repeated expressions into well-named variables, simplify complex
  boolean logic, use proper constant declarations, and remove redundant code that
  sets default values.'
repository: facebook/yoga
label: Code Style
language: C++
comments_count: 4
repository_stars: 18255
---

Enhance code clarity and maintainability by applying several readability techniques: extract repeated expressions into well-named variables, simplify complex boolean logic, use proper constant declarations, and remove redundant code that sets default values.

Key practices:
- Extract repeated expressions: When the same complex expression appears multiple times, extract it into a descriptive variable (e.g., `mainAxisDim` for `node->getLayout().measuredDimensions[dim[mainAxis]]`)
- Simplify complex boolean expressions: Remove redundant parentheses and restructure logic for better visual parsing
- Use proper constant declarations: Prefer `constexpr bool kConstantName = false;` over preprocessor defines or global variables
- Remove redundant default assignments: Don't explicitly set values that are already defaults (e.g., `YGJustifyFlexStart` is the default for justify content)

Example of extracting repeated expressions:
```cpp
// Before
child->getLeadingPosition(mainAxis, node->getLayout().measuredDimensions[dim[mainAxis]])
child->getLeadingMargin(mainAxis, node->getLayout().measuredDimensions[dim[mainAxis]])

// After  
const auto mainAxisDim = node->getLayout().measuredDimensions[dim[mainAxis]];
child->getLeadingPosition(mainAxis, mainAxisDim)
child->getLeadingMargin(mainAxis, mainAxisDim)
```