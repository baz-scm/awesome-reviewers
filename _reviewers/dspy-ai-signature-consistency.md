---
title: AI signature consistency
description: Ensure AI model signatures maintain consistency between field types and
  descriptions, and avoid redundant prompting techniques when the desired behavior
  is already captured in the signature definition.
repository: stanfordnlp/dspy
label: AI
language: Other
comments_count: 2
repository_stars: 27813
---

Ensure AI model signatures maintain consistency between field types and descriptions, and avoid redundant prompting techniques when the desired behavior is already captured in the signature definition.

When defining AI model signatures, field descriptions should accurately reflect the actual data type. For example, if a field accepts `List[dspy.Image]`, the description should indicate "A list of images" rather than "An image".

Additionally, avoid using redundant prompting techniques like ChainOfThought when the signature already includes fields that capture the desired reasoning or explanation output.

Example of good practice:
```python
class ColorSignature(dspy.Signature):
    """Output the color of the designated image."""
    images: List[dspy.Image] = dspy.InputField(desc="A list of images")
    explanation = dspy.OutputField(desc="Reasoning for color detection")
    color = dspy.OutputField(desc="Detected color")

# Use simple Predict instead of ChainOfThought since explanation field exists
class ColorModule(dspy.Module):
    def __init__(self):
        self.prog = dspy.Predict(ColorSignature)  # Not dspy.ChainOfThought
```

This approach reduces confusion, eliminates redundancy, and ensures that AI model interfaces are clear and maintainable.