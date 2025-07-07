---
title: Informative error messages
description: 'Error messages should be informative, actionable, and concise to help
  users quickly understand and fix issues. Follow these guidelines:


  1. Include specific details in error messages:'
repository: tensorflow/tensorflow
label: Error Handling
language: Python
comments_count: 5
repository_stars: 190625
---

Error messages should be informative, actionable, and concise to help users quickly understand and fix issues. Follow these guidelines:

1. Include specific details in error messages:
   - Parameter names and values causing the error
   - Valid ranges or expected types
   - Actual values that violated constraints

2. Use modern f-strings for better readability:
   ```python
   # Avoid
   raise ValueError('Invalid axis: {} not in range {}-{}'.format(axis, min_val, max_val))
   
   # Prefer
   raise ValueError(f"Argument `axis` = {axis} not in range [{min_val}, {max_val})")
   ```

3. Keep messages focused and concise:
   ```python
   # Too verbose
   raise ValueError(f'Python found at {python_bin_path} is not version 3. Please update to the latest version to continue with installation.')
   
   # Better
   raise ValueError(f'Python from {python_bin_path} is not version 3.')
   ```

4. For validation errors, include both the expected and actual values:
   ```python
   # Vague
   raise ValueError("Type annotation does not match input_signature")
   
   # Better
   raise ValueError(f"Type annotation for argument '{arg}' expected {annotation_dtype} but input_signature specified {input_signature_dtype}")
   ```

Well-crafted error messages reduce debugging time and improve the overall developer experience when using your code.