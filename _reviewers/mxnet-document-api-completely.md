---
title: Document API completely
description: 'Always provide comprehensive API documentation that clearly specifies:


  1. **Parameter types** - Document all acceptable parameter types, not just specific
  implementations. When a parameter accepts any object that satisfies certain behavior
  (like iterables), explicitly state this rather than referencing a specific class.'
repository: apache/mxnet
label: API
language: Python
comments_count: 3
repository_stars: 20801
---

Always provide comprehensive API documentation that clearly specifies:

1. **Parameter types** - Document all acceptable parameter types, not just specific implementations. When a parameter accepts any object that satisfies certain behavior (like iterables), explicitly state this rather than referencing a specific class.

2. **Function aliases** - When implementing function aliases (like `acos` for `arccos` or `pow` for `power`), clearly document their relationship to the original function and explain why the alias exists.

3. **Standards compliance** - Reference any industry standards or specifications that the API follows, especially when they might differ from what users expect.

Example:
```python
def process_data(data_source, options=None):
    """Process data from the provided source.
    
    Parameters
    ----------
    data_source : iterable object
        Any iterable that yields data batches. This can be a DataLoader 
        instance, a list of arrays, or any custom iterable implementing 
        the required interface.
    options : dict, optional
        Processing options.
        
    Notes
    -----
    This function follows the data processing standards specified in
    https://example.org/standards/data-processing.
    """
```

Or when documenting aliases:
```python
acos = arccos
acos.__doc__ = """
    Trigonometric inverse cosine, element-wise.
    
    Notes
    ----------
    `acos` is an alias for `arccos`. It is a standard API in
    https://data-apis.org/array-api/latest/ instead of an official NumPy 
    operator.
    
    >>> np.acos is np.arccos
    True
"""
```
