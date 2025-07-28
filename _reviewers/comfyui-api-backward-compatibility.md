---
title: API backward compatibility
description: Ensure API changes maintain backward compatibility to avoid breaking
  existing clients and workflows. When adding new functionality, use optional parameters
  with sensible defaults rather than required parameters. When versioning APIs, follow
  the `/api/v2/resource` pattern and maintain deprecated endpoints during transition
  periods to allow clients time to...
repository: comfyanonymous/ComfyUI
label: API
language: Python
comments_count: 5
repository_stars: 83726
---

Ensure API changes maintain backward compatibility to avoid breaking existing clients and workflows. When adding new functionality, use optional parameters with sensible defaults rather than required parameters. When versioning APIs, follow the `/api/v2/resource` pattern and maintain deprecated endpoints during transition periods to allow clients time to migrate.

Key practices:
- Add new parameters under "optional" sections with default values to prevent breaking saved workflows
- Maintain existing API endpoints when introducing new versions until clients can migrate
- Use proper versioning patterns like `/api/v2/userdata` rather than `/userdata-v2`
- Plan migration strategies that allow both old and new APIs to coexist temporarily

Example of backward-compatible parameter addition:
```python
def INPUT_TYPES(s):
    return {
        "required": {
            "images": ("IMAGE", ),
            "filename_prefix": ("STRING", {"default": "ComfyUI"})
        },
        "optional": {
            "disable_metadata": ("BOOLEAN", {"default": False})  # New parameter as optional
        }
    }
```

This approach prevents breaking existing API workflows while enabling new functionality for clients that choose to adopt it.