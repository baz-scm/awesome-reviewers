---
title: Memoize expensive operations
description: Cache results of expensive operations, especially shell commands and
  external queries, to avoid redundant executions. Use Ruby's idiomatic memoization
  pattern with blocks for clarity and efficiency. Only fetch data when needed, and
  structure code to optimize for the most common execution paths.
repository: chef/chef
label: Performance Optimization
language: Ruby
comments_count: 6
repository_stars: 7860
---

Cache results of expensive operations, especially shell commands and external queries, to avoid redundant executions. Use Ruby's idiomatic memoization pattern with blocks for clarity and efficiency. Only fetch data when needed, and structure code to optimize for the most common execution paths.

For shell commands:
```ruby
def choco_version
  @choco_version ||= begin
    powershell_exec!("choco --version").result
  end
end
```

For conditional resource initialization:
```ruby
def loop_mount_points
  # Only fetch when actually needed
  @loop_mount_points ||= shell_out!("losetup -a").stdout
end
```

When executing shell commands, use splat arguments instead of string concatenation:
```ruby
# Prefer this (avoids shell parsing overhead):
shell_out!(systemctl_path, args, "show", "-p", "UnitFileState", new_resource.service_name, options)

# Instead of:
shell_out!("#{systemctl_path} #{args} show -p UnitFileState #{new_resource.service_name}", options)
```

For frequently accessed data, consider optimizing for the most common case:
```ruby
# Optimization for the 90% single-package case
target_dirs = []
target_dirs << targets.first.downcase if targets.length == 1
```

Always benchmark critical code paths before and after optimization to verify improvements.
