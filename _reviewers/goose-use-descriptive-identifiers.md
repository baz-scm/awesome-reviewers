---
title: Use descriptive identifiers
description: 'Replace generic, ambiguous, or magic identifiers with descriptive, specific
  names that clearly communicate intent and avoid confusion.


  Key principles:'
repository: block/goose
label: Naming Conventions
language: Rust
comments_count: 6
repository_stars: 19037
---

Replace generic, ambiguous, or magic identifiers with descriptive, specific names that clearly communicate intent and avoid confusion.

Key principles:
- Avoid time-based or generic IDs - use UUIDs or semantic identifiers instead
- Replace overloaded terms with specific names (e.g., "is_tool_router_enabled" instead of "get_router_tool_selection_strategy")  
- Use named constants instead of magic numbers with comments
- Prefer enums over string constants for type safety
- Maintain consistent terminology across the codebase

Examples:

```rust
// Bad: Generic time-based ID
let execution_id = format!("exec_{}", SystemTime::now().duration_since(UNIX_EPOCH));

// Good: UUID-based ID  
let execution_id = format!("exec_{}", Uuid::new_v4());

// Bad: Magic number with comment
command.creation_flags(0x08000000); // CREATE_NO_WINDOW flag

// Good: Named constant
const CREATE_NO_WINDOW: u32 = 0x08000000;
command.creation_flags(CREATE_NO_WINDOW);

// Bad: String constants
const EXECUTION_MODE_PARALLEL: &str = "parallel";
const EXECUTION_MODE_SEQUENTIAL: &str = "sequential";

// Good: Enum
enum ExecutionMode {
    Parallel,
    Sequential,
}
```

This approach improves code maintainability, reduces ambiguity, and makes the codebase more self-documenting.