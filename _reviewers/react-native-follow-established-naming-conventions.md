---
title: Follow established naming conventions
description: Ensure all identifiers (variables, methods, classes) adhere to the project's
  established naming conventions and accurately reflect their purpose. Consistency
  in naming patterns improves code readability and maintainability across the codebase.
repository: facebook/react-native
label: Naming Conventions
language: Ruby
comments_count: 2
repository_stars: 123178
---

Ensure all identifiers (variables, methods, classes) adhere to the project's established naming conventions and accurately reflect their purpose. Consistency in naming patterns improves code readability and maintainability across the codebase.

Key principles:
- Follow documented naming conventions (e.g., "REACT_NATIVE is shortened to RCT")
- Use semantically clear names that match the actual behavior
- Maintain consistency with existing patterns in the codebase

Example from codebase:
```ruby
# Instead of inconsistent naming:
REACT_NATIVE_DEPS_BUILD_FROM_SOURCE

# Follow the established convention:
RCT_USE_DEP_PREBUILD

# Ensure method names match their actual purpose:
# If method handles release builds, name it appropriately
def podspec_source_download_prebuild_release_tarball()
    url = release_tarball_url(@@react_native_version, :release) # not :debug
end
```

Before introducing new naming patterns, verify they align with existing conventions or update documentation if establishing new standards.