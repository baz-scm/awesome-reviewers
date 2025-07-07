---
title: Complete docstring structure
description: 'Function documentation should follow a consistent structure that includes
  all necessary components to be complete and usable. Each docstring should:


  1. Start with a one-line summary that concisely describes the function''s purpose'
repository: tensorflow/tensorflow
label: Documentation
language: Python
comments_count: 4
repository_stars: 190625
---

Function documentation should follow a consistent structure that includes all necessary components to be complete and usable. Each docstring should:

1. Start with a one-line summary that concisely describes the function's purpose
2. Include an "Args" section that documents all parameters
3. Format "Returns" section as noun phrases (not full sentences)
4. Document exceptions when relevant

Example of proper docstring structure:

```python
def is_platform_supported(precision, gpu_id=0):
  """Determines if the current NVIDIA GPU platform supports the requested precision.
  
  Required Compute Capabilities:
  - FP16 = 5.3 || 6.0 || 6.2 || 7.0+
  - INT8 = 6.1 || 7.0 || 7.2+
  
  Args:
    precision: String indicating the desired compute precision.
    gpu_id: Integer ID of the GPU to check. Defaults to 0.
    
  Returns:
    Boolean indicating whether the platform supports the requested precision.
    
  Raises:
    ValueError: If precision is not a supported value.
  """
```

Following this structure ensures documentation is consistent, complete, and meets style guidelines. It helps other developers understand your code more quickly and makes automated documentation generation more effective.