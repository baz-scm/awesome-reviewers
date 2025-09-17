---
title: Configuration value types
description: 'Ensure configuration values use appropriate types, avoid unnecessary
  Optional annotations, and maintain consistency in data formats and units.


  Key principles:'
repository: langgenius/dify
label: Configurations
language: Python
comments_count: 5
repository_stars: 114231
---

Ensure configuration values use appropriate types, avoid unnecessary Optional annotations, and maintain consistency in data formats and units.

Key principles:
1. **Use explicit boolean types** instead of string representations when the configuration is consumed as a boolean
2. **Avoid Optional for fields with defaults** - if a default value is provided, Optional is redundant
3. **Choose consistent time units** across related configurations (prefer seconds for precision, minutes for readability)
4. **Use appropriate data formats** - prefer unix timestamps over ISO strings for simplicity and timezone safety

Example of proper configuration typing:
```python
class MyConfig(BaseSettings):
    # Good: explicit boolean with default
    SSL_VERIFY: bool = Field(default=True)
    
    # Bad: unnecessary Optional with default
    # SSL_VERIFY: Optional[bool] = Field(default=True)
    
    # Good: consistent time unit choice
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Good: unix timestamp for cache keys
    def get_cache_timestamp(self) -> int:
        return int(datetime.now().timestamp())
```

This approach reduces configuration complexity, improves type safety, and ensures consistent behavior across different deployment environments.