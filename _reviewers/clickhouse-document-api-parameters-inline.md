---
title: Document API parameters inline
description: When designing APIs, prioritize clarity and self-documentation by adding
  inline comments for non-obvious parameters and choosing descriptive method names.
  This reduces the need for external documentation and makes the code more maintainable.
repository: ClickHouse/ClickHouse
label: API
language: Other
comments_count: 2
repository_stars: 42425
---

When designing APIs, prioritize clarity and self-documentation by adding inline comments for non-obvious parameters and choosing descriptive method names. This reduces the need for external documentation and makes the code more maintainable.

For boolean parameters or complex arguments, include inline comments that explain their purpose:

```cpp
// Good: Clear parameter documentation
void setRawPath(const Path & path_) override { 
    path = {path_.path, /* allow_partial_prefix */false}; 
}

// Good: Descriptive method names with explanatory comments
/// Unlike s3 and azure, which are object storages,
/// hdfs is a filesystem, so it cannot list files by partial prefix,
/// only by directory.
Path getRawPath() const override { return path; }
```

Additionally, consider feature detection over versioning when possible to maintain backward compatibility and reduce API complexity. Well-documented APIs reduce the cognitive load on developers and prevent misuse of parameters or methods.