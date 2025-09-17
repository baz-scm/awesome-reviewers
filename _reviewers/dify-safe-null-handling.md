---
title: Safe null handling
description: Handle null and undefined values safely by using appropriate fallback
  patterns, validating critical parameters early, and avoiding mutable default arguments.
repository: langgenius/dify
label: Null Handling
language: Python
comments_count: 10
repository_stars: 114231
---

Handle null and undefined values safely by using appropriate fallback patterns, validating critical parameters early, and avoiding mutable default arguments.

**Key Practices:**

1. **Use safe fallback patterns** for optional values:
```python
# Good: Safe fallback with or operator
cpu_count = os.cpu_count() or 4
meta = meta or {}

# Good: Safe attribute access with getattr
func_name = getattr(func, "__name__", "Unknown")

# Avoid: Direct access that might fail
func_name = func.__name__  # May raise AttributeError
```

2. **Validate critical parameters early** and fail fast:
```python
# Good: Early validation with clear error
def get_features(tenant_id: str):
    if not tenant_id:
        raise ValueError("tenant_id is required")
    # ... rest of function

# Avoid: Allowing empty/None values to propagate
def get_features(tenant_id: str):
    # ... function continues without validation
```

3. **Avoid mutable default arguments**:
```python
# Good: Use None and assign in function body
def create_blob_message(blob: bytes, meta: dict = None, save_as: str = ""):
    meta = meta or {}

# Good: Use default_factory for Pydantic models
conditions: list[SubCondition] = Field(default_factory=list)

# Avoid: Mutable default argument
def create_blob_message(blob: bytes, meta: dict = {}, save_as: str = ""):
```

4. **Use dict.get() with explicit defaults** for safe dictionary access:
```python
# Good: Explicit default value
for tool in agent_mode.get("tools", []):

# Less clear: Relying on or operator
for tool in agent_mode.get("tools") or []:
```

5. **Be explicit about parameter validation**:
```python
# Good: Check parameter before use
if keyword and isinstance(keyword, str):
    keyword_like_val = f"%{keyword[:30]}%"

# Avoid: Using parameter without validation
keyword_like_val = f"%{keyword[:30]}%"  # May fail if keyword is None
```

This approach prevents runtime errors, makes code more predictable, and clearly communicates intent about required vs optional values.