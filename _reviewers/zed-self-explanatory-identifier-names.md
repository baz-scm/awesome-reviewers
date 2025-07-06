---
title: Self-explanatory identifier names
description: Choose identifier names that clearly convey their purpose without requiring
  users to understand implementation details. If reviewers struggle to understand
  what a name means, it likely needs improvement.
repository: zed-industries/zed
label: Naming Conventions
language: Json
comments_count: 3
repository_stars: 62119
---

Choose identifier names that clearly convey their purpose without requiring users to understand implementation details. If reviewers struggle to understand what a name means, it likely needs improvement.

When naming functions or settings:
1. Favor descriptive clarity over excessive brevity
2. Remove redundant parts while maintaining meaning
3. When boolean names become awkward, consider using enums instead

**Examples:**
```
// Less clear
"line_number_base_width": 4

// Better - describes what it actually means
"min_line_number_digits": 4
```

```
// Unclear boolean (what does "true" actually mean?)
"focus_skip_active_file": true

// Better as an enum
enum AutoFocus {
    First,
    SkipActive
}
```

```
// Unnecessarily verbose
"workspace::IncreaseOpenDocksSizeByOffset"

// Better - removes redundancy while preserving meaning
"workspace::IncreaseDocksSize"
```