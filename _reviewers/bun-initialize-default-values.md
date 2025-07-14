---
title: Initialize default values
description: 'Always initialize class attributes with default values to prevent AttributeError
  exceptions when accessing potentially undefined values. Use defensive coding patterns:'
repository: oven-sh/bun
label: Null Handling
language: Python
comments_count: 2
repository_stars: 79093
---

Always initialize class attributes with default values to prevent AttributeError exceptions when accessing potentially undefined values. Use defensive coding patterns:

1. Set default values in `__init__()` for critical attributes
2. Initialize attributes with safe fallback values in exception handlers
3. Use defensive checks (e.g., `hasattr()`) before accessing attributes that might be undefined

Example:
```python
def update(self):
    # Initialize with defaults before try block
    self.len = 0
    self.cap = 0
    self.ptr = None
    self.elem_type = None
    self.elem_size = 0
    
    try:
        self.ptr = self.value.GetChildMemberWithName('ptr')
        self.len = self.value.GetChildMemberWithName('len').unsigned
        self.cap = self.value.GetChildMemberWithName('cap').unsigned
        self.elem_type = self.ptr.type.GetPointeeType()
        self.elem_size = self.elem_type.size
    except:
        # Already have default values
        pass
        
def get_child_at_index(self, index):
    if index not in range(self.len): 
        return None
    try: 
        if not hasattr(self, 'ptr') or not hasattr(self, 'elem_size') or not hasattr(self, 'elem_type'):
            return None
        return self.ptr.CreateChildAtOffset('[%d]' % index, index * self.elem_size, self.elem_type)
    except: 
        return None
```

This pattern ensures your code is resilient to initialization failures and prevents null reference issues in dependent methods.