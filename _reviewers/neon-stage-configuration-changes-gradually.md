---
title: Stage configuration changes gradually
description: 'When introducing configuration changes that affect multiple system components,
  implement them in stages to ensure smooth transitions and backward compatibility.
  Follow these steps:'
repository: neondatabase/neon
label: Configurations
language: Rust
comments_count: 5
repository_stars: 19015
---

When introducing configuration changes that affect multiple system components, implement them in stages to ensure smooth transitions and backward compatibility. Follow these steps:

1. Add new configuration option while maintaining old one
2. Wait for new option to reach release
3. Switch to new option in dependent components
4. Remove old option after full migration

Example:
```rust
// Step 1: Add new option while keeping old
impl Config {
    fn get_safekeeper_info(&self) -> String {
        // Support both old and new formats
        self.safekeeper_connstrings.clone()
            .or_else(|| self.safekeepers.map(|s| convert_to_new_format(s)))
            .unwrap_or_default()
    }
}

// Step 2: Wait for release with dual support

// Step 3: Switch dependent components to new format
conf.append("neon.safekeeper_connstrings", &safekeepers);
// Instead of old: conf.append("neon.safekeepers", &safekeepers);

// Step 4: Remove old option in future release
```

This approach:
- Prevents breaking changes in production
- Allows gradual testing in staging/pre-prod
- Maintains backward compatibility during transition
- Reduces deployment risks through phased rollout