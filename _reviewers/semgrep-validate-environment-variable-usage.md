---
title: validate environment variable usage
description: Always validate environment variables with proper fallback logic and
  avoid unnecessary usage in tests or when defaults suffice. Check for truthiness
  rather than explicit None comparisons to handle empty strings, and ensure configuration
  values match their declared types and intended usage.
repository: semgrep/semgrep
label: Configurations
language: Python
comments_count: 4
repository_stars: 12598
---

Always validate environment variables with proper fallback logic and avoid unnecessary usage in tests or when defaults suffice. Check for truthiness rather than explicit None comparisons to handle empty strings, and ensure configuration values match their declared types and intended usage.

Key practices:
- Use truthiness checks: `if cache_home and Path(cache_home).is_dir()` instead of `if cache_home is None`
- Provide sensible fallbacks for missing or invalid environment variables
- Remove unnecessary `env.get()` calls in tests when the environment variable is never set
- Validate that configuration settings match their actual behavior (e.g., output_format="json" should produce JSON, not text)

Example from XDG cache directory handling:
```python
cache_home = os.getenv("XDG_CACHE_HOME")
if cache_home and Path(cache_home).is_dir():
    parent_dir = Path(cache_home)
else:
    parent_dir = Path.home() / ".cache"
```

This approach handles both None values and empty strings while providing a clear fallback path.