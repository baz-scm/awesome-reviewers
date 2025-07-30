---
title: validate configuration defaults
description: Configuration parameters should be properly validated with appropriate
  defaults and clear handling of edge cases. Avoid using arbitrary defaults when values
  should be explicitly required, and ensure configuration validation distinguishes
  between None, empty, and zero values.
repository: Unstructured-IO/unstructured
label: Configurations
language: Python
comments_count: 9
repository_stars: 12116
---

Configuration parameters should be properly validated with appropriate defaults and clear handling of edge cases. Avoid using arbitrary defaults when values should be explicitly required, and ensure configuration validation distinguishes between None, empty, and zero values.

Key practices:
1. **Validate parameter types and ranges** - Check that configuration values meet expected constraints
2. **Use meaningful defaults** - Set defaults that make sense for the use case, not just convenient values
3. **Handle None vs zero distinction** - Be explicit about whether 0 is a valid value or should trigger default behavior
4. **Filter unsupported parameters** - Remove configuration options not supported by the current version
5. **Make critical configs required** - Don't provide defaults for parameters that users should explicitly set

Example of proper configuration validation:
```python
@property
def TESSERACT_CHARACTER_CONFIDENCE_THRESHOLD(self) -> float:
    """Tesseract predictions with confidence below this threshold are ignored"""
    return self._get_float("TESSERACT_CHARACTER_CONFIDENCE_THRESHOLD", 0.0)

def get_retries_config(self, retries_initial_interval: Optional[int]) -> Optional[retries.RetryConfig]:
    # Check for None explicitly, not just falsy values
    if retries_initial_interval is not None:
        return retries_initial_interval
    return DEFAULT_RETRIES_INITIAL_INTERVAL_SEC

# Filter configuration to supported fields only
possible_fields = [f.name for f in fields(PartitionParameters)]
filtered_config = {k: v for k, v in config.items() if k in possible_fields}
```

This prevents configuration errors, improves user experience, and ensures consistent behavior across different environments and versions.