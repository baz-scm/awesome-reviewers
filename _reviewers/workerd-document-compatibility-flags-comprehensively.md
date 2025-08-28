---
title: Document compatibility flags comprehensively
description: All compatibility flags must include comprehensive documentation that
  clearly explains their purpose, behavior, timing, and relationships with other flags.
  This documentation should follow a consistent format and provide sufficient context
  for developers to understand the flag's impact.
repository: cloudflare/workerd
label: Configurations
language: Other
comments_count: 7
repository_stars: 6989
---

All compatibility flags must include comprehensive documentation that clearly explains their purpose, behavior, timing, and relationships with other flags. This documentation should follow a consistent format and provide sufficient context for developers to understand the flag's impact.

Required documentation elements:
- Clear description of what the flag enables or disables
- Explanation of when the flag takes effect (dates, conditions)
- Relationships with other flags (mutual exclusivity, dependencies, implications)
- Impact on existing functionality and backward compatibility

Example of proper flag documentation:
```
removeNodejsCompatEOLv22 @117 :Bool
    $compatEnableFlag("remove_nodejs_compat_eol_v22")
    $compatDisableFlag("add_nodejs_compat_eol_v22")
    $impliedByAfterDate(name = "removeNodejsCompatEOL", date = "2027-04-30");
# Removes APIs that reached end-of-life in Node.js 22.x. When using the
# removeNodejsCompatEOL flag, this will default enable on/after 2027-04-30.
```

For complex flag relationships, document dependencies explicitly:
```
# Requires both "enable_nodejs_http_modules" and "enable_nodejs_http_server_modules"
# to be enabled. The type stripping flag is mutually exclusive and will take 
# precedence if both happen to be defined.
```

This ensures developers understand flag behavior, prevents configuration errors, and maintains consistency across the codebase.