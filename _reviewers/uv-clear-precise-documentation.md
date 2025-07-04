---
title: Clear precise documentation
description: Documentation should use direct, precise language that accurately describes
  components and their behavior. Maintain consistent grammatical structure throughout
  related documentation sections for improved readability.
repository: astral-sh/uv
label: Documentation
language: Rust
comments_count: 8
repository_stars: 60322
---

Documentation should use direct, precise language that accurately describes components and their behavior. Maintain consistent grammatical structure throughout related documentation sections for improved readability.

For command-line options and parameters:
- Use direct statements rather than "Whether to..." phrasing when possible
- Clearly state both what an option does and the default behavior it modifies
- Be specific about the purpose and constraints of parameters

Example improvements:
```diff
- /// Whether to prefer uv-managed or system Python installations.
+ /// Disable use of uv-managed Python distributions.
+ ///
+ /// Instead, uv will search for a suitable Python installation on the system.

- /// Only print the final value
+ /// Only show the version
+ ///
+ /// By default, uv will show the project name before the version.

- /// The directory to store the Python installation in.
+ /// The directory Python installations are stored in.

- /// Upgrades will not remove lower installed patch versions.
+ /// During an upgrade, uv will not uninstall outdated patch versions.
```

For grammatical consistency, maintain the same tense within related sections, especially in enums where options are presented together. This improves scanning and comprehension of documentation.