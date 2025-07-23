---
title: Document configurations completely
description: 'Ensure configuration documentation is comprehensive, clear and actionable
  for developers. This includes:


  1. **Document all possible configuration options and behaviors**, not just defaults:'
repository: continuedev/continue
label: Configurations
language: Other
comments_count: 3
repository_stars: 27819
---

Ensure configuration documentation is comprehensive, clear and actionable for developers. This includes:

1. **Document all possible configuration options and behaviors**, not just defaults:
```yaml
# Good example: Explicitly documenting all behaviors
- alwaysApply: true    # Always include the rule, regardless of file context
- alwaysApply: false   # Only include if globs exist AND match file context
- alwaysApply: undefined # Default: include if no globs exist OR globs exist and match
```

2. **Clearly document configuration storage locations** with platform-specific paths:
```
Configuration is stored in ~/.continue directory (or %USERPROFILE%\.continue on Windows)
```

3. **Use consistent, platform-appropriate formats** for configuration examples. When showing multiple formats (YAML/JSON), use the appropriate tab components for your documentation system:

```jsx
<Tab title="YAML">
  // YAML configuration example
</Tab>
<Tab title="JSON">
  // JSON configuration example  
</Tab>
```

Proper configuration documentation reduces developer confusion, prevents misconfigurations, and simplifies troubleshooting.