---
title: Write clean, maintainable code
description: 'Focus on writing clean and maintainable code that''s easy to read and
  reason about. This involves several key practices:


  1. **Use list comprehensions instead of manual loops** when collecting or transforming
  data:'
repository: pytorch/pytorch
label: Code Style
language: Python
comments_count: 6
repository_stars: 91169
---

Focus on writing clean and maintainable code that's easy to read and reason about. This involves several key practices:

1. **Use list comprehensions instead of manual loops** when collecting or transforming data:

```python
# Instead of this:
aotriton_image_path = os.path.join(lib_path, "aotriton.images")
aks2_files = []
for root, dirs, files in os.walk(aotriton_image_path):
    subpath = os.path.relpath(root, start=aotriton_image_path)
    for fn in files:
        aks2_files.append(os.path.join("lib/aotriton.images", subpath, fn))

# Do this:
aotriton_image_path = TORCH_DIR / "lib" / "aotriton.images"
aks2_files = [
    file.relative_to(TORCH_DIR).as_posix()
    for file in aotriton_image_path.rglob("*")
    if file.is_file()
]
```

2. **Keep functional changes separate from formatting changes**. This makes code reviews clearer and simplifies identifying the actual logic changes.

3. **Use early returns to reduce nesting**:

```python
# Instead of this:
if isinstance(self, ExternKernel):
    if op is not None:
        # ... more code ...

# Do this:
if not isinstance(self, ExternKernel) or op is None:
     return None
# ... more code ...
```

4. **Eliminate unnecessary temporary variables**:

```python
# Instead of this:
ret = flop_counter_mode.get_total_flops()
return ret

# Do this:
return flop_counter_mode.get_total_flops()
```

5. **Remove debug print statements** before committing code:

```python
# Remove lines like:
print(f"{op_name}, {strategy.strategies}")
```

6. **Avoid code duplication** by using loops or appropriate abstractions:

```python
# Instead of sequential checks:
if mgr_name == "":
    rc, _, _ = run("which dpkg")
    if rc == 0:
        mgr_name = "dpkg"
if mgr_name == "":
    rc, _, _ = run("which dnf")
    if rc == 0:
        mgr_name = "dnf"

# Use a loop:
for mgr_name in ["dpkg", "dnf", "yum", "zypper", ""]:
    if mgr_name == "":
        continue
    rc, _, _ = run(f"which {mgr_name}")
    if rc == 0:
        break
```

These practices significantly improve code readability, reduce bugs, and make maintenance easier for everyone working with the codebase.
