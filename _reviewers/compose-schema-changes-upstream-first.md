---
title: Schema changes upstream first
description: When modifying configuration schemas, always propose changes to the upstream/source
  repository first before implementing them locally. This practice prevents schema
  divergence, maintains version integrity, and ensures a single source of truth for
  configuration definitions.
repository: docker/compose
label: Configurations
language: Json
comments_count: 3
repository_stars: 35858
---

When modifying configuration schemas, always propose changes to the upstream/source repository first before implementing them locally. This practice prevents schema divergence, maintains version integrity, and ensures a single source of truth for configuration definitions.

Key principles:
- Never modify already released schema versions - use newer versions for new features
- Submit changes to upstream repositories (like compose-spec) before local implementation
- Reference upstream schemas as the authoritative source rather than maintaining local copies
- Consolidate schema management to avoid inconsistencies across different versions

Example from the discussions:
```json
// Instead of directly modifying local schema files
"secrets": {"$ref": "#/definitions/build_secrets"}

// First propose the change to upstream compose-spec repository
// Then reference the updated upstream schema
```

This approach ensures configuration schemas remain consistent across the ecosystem and prevents the fragmentation that occurs when teams make isolated changes to shared configuration standards.