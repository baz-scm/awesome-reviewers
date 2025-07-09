---
title: Environment-specific config defaults
description: Define appropriate configuration defaults for different environments
  (development, testing, production) using dedicated configuration classes with sensible
  defaults. When test environments require different configurations than production,
  explicitly create separate config structures rather than hardcoding values throughout
  tests.
repository: neondatabase/neon
label: Configurations
language: Python
comments_count: 3
repository_stars: 19015
---

Define appropriate configuration defaults for different environments (development, testing, production) using dedicated configuration classes with sensible defaults. When test environments require different configurations than production, explicitly create separate config structures rather than hardcoding values throughout tests.

When handling external dependencies in test configurations, vendor them rather than downloading at runtime to ensure test reliability and eliminate network dependencies.

Example:
```python
@dataclass
class PageserverTestConfig:
    # Test-specific defaults that differ from production
    page_cache_size: int = 16384
    max_file_descriptors: int = 500000
    
    @staticmethod
    def default() -> PageserverTestConfig:
        return PageserverTestConfig(
            # Override with test-appropriate values
        )

# Usage
neon_env_builder.pageserver_config_override = f"page_cache_size={config.page_cache_size}; max_file_descriptors={config.max_file_descriptors}"
```

This approach ensures configurations are consistent, properly defaulted, and environment-appropriate without spreading hardcoded values throughout the codebase.