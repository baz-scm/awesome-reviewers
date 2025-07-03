---
title: Extract and organize methods
description: Break down large, complex methods into smaller, focused methods with
  clear names that describe their purpose. This improves code readability, maintainability,
  and testability.
repository: chef/chef
label: Code Style
language: Ruby
comments_count: 8
repository_stars: 7860
---

Break down large, complex methods into smaller, focused methods with clear names that describe their purpose. This improves code readability, maintainability, and testability.

When methods grow too long or handle multiple concerns:
- Extract separate behaviors into dedicated methods
- Use descriptive method names that explain their purpose
- Avoid duplicating logic across methods

For example, instead of:

```ruby
def wrapper_script
  # 50+ lines of complex code with slight variations
  if new_resource.use_inline_powershell
    # inline powershell version
  else
    # regular shell out version
  end
end
```

Refactor to:

```ruby
def wrapper_script
  if new_resource.use_inline_powershell
    inline_powershell_wrapper_script
  else
    shell_out_wrapper_script
  end
end

def inline_powershell_wrapper_script
  # inline powershell implementation
end

def shell_out_wrapper_script
  # regular shell out implementation
end
```

Or when logic is repeated:

```ruby
def resolved_package(pkg)
  new_resource.anchor_package_regex ? "^#{pkg}$" : pkg
end
```

This approach reduces cognitive load, improves reusability, and makes code easier to understand and modify.
