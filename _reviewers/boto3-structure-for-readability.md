---
title: Structure for readability
description: 'Prioritize code readability by structuring code in a way that makes
  it easy to understand at a glance. This includes:


  1. Break complex conditions into clearer if-else blocks for better comprehension:'
repository: boto/boto3
label: Code Style
language: Python
comments_count: 4
repository_stars: 9417
---

Prioritize code readability by structuring code in a way that makes it easy to understand at a glance. This includes:

1. Break complex conditions into clearer if-else blocks for better comprehension:
```python
# Instead of this:
if account_id and access_key is None and secret_key is None:
    return True

# Prefer this:
if account_id is None:
    return False
elif access_key is None or secret_key is None:
    return True
return False
```

2. Use higher-level APIs when they express intent more clearly:
```python
# Instead of this:
path = os.sep.join([self.EXAMPLE_PATH, self._service_name + '.rst'])

# Prefer this:
path = os.path.join(self.EXAMPLE_PATH, self._service_name + '.rst')
```

3. Always use explicit `is not None` when comparing against None:
```python
# Instead of this:
if identifiers or identifiers == None:
    
# Prefer this:
if identifiers is not None:
```

4. Use named parameters for complex function calls to improve readability:
```python
# Instead of this with nested dictionaries:
resource = self.load('test', 'Message', model, defs, None)

# Prefer this:
resource = self.load(
    service_name='test', 
    resource_name='Message',
    model=model,
    resource_defs=defs,
    service_model=None
)
```

These practices help other developers understand your code faster and reduce the cognitive load when navigating the codebase.