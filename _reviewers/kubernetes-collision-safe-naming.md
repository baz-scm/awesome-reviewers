---
title: Collision-Safe Naming
description: 'Use standardized, collision-resistant naming for public identifiers—especially
  versioned module paths and generated-code symbols.


  Apply this in two common cases:'
repository: kUbernetes/kUbernetes
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 128688
---

Use standardized, collision-resistant naming for public identifiers—especially versioned module paths and generated-code symbols.

Apply this in two common cases:

1) Module/version identifiers
- Tag releases with proper semver (e.g., `v4.0.0`), not just `v4`.
- Ensure versioned import paths match the major version (e.g., update imports to `.../pkg/iptables/v4` when moving to a v4-tagged release).

2) Constrained API fields (enums)
- Prefer `enum` over `string` when the field has a fixed set of allowed values.
- Choose enum value names that won’t collide under generated-language scoping rules; use a consistent prefix based on the full enum name.

Example (proto):
```proto
message LinuxContainerSecurityContext {
  enum CgroupMountMode {
    CGROUP_MOUNT_MODE_READ_ONLY = 0;
    CGROUP_MOUNT_MODE_WRITABLE  = 1;
  }

  CgroupMountMode cgroup_mount_mode = 18;
}
```

Result: builds don’t unexpectedly treat versions as SHAs, imports stay consistent across major versions, and generated symbols remain stable and collision-free.