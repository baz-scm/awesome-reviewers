---
title: Use if-unwrap with optionals
description: Always use Zig's if-unwrap pattern (`if (optional) |value| {...}`) when
  working with optional values instead of forced unwrapping with `.?`. This pattern
  is safer as it avoids runtime panics, more readable, and aligns with Zig's idioms
  for null safety.
repository: ghostty-org/ghostty
label: Null Handling
language: Other
comments_count: 5
repository_stars: 32864
---

Always use Zig's if-unwrap pattern (`if (optional) |value| {...}`) when working with optional values instead of forced unwrapping with `.?`. This pattern is safer as it avoids runtime panics, more readable, and aligns with Zig's idioms for null safety.

When checking an optional only to see if it's not null and discarding the value, use `!= null` instead of additional syntax. When you need to use the value, use the if-unwrap pattern to create a new non-optional variable in a limited scope:

```zig
// Bad - prone to crashes if null
if (self.current_background_image != null) {
    switch (self.current_background_image.?) {
        .ready => {},
        // ...
    }
}

// Good - compiler enforced null safety
if (self.current_background_image) |current_background_image| {
    switch (current_background_image) {
        .ready => {},
        // ...
    }
}

// Bad - will crash if background-image is null
const background_image = try config.@"background-image".?.clone(alloc);

// Good - handles null case explicitly
const background_image = if (config.@"background-image") |v| try v.clone(alloc) else null;

// Alternative approach - early return
const current_background_image = self.current_background_image orelse return;
// Now use current_background_image without unwrapping
```

This approach not only prevents runtime crashes but also makes the code's intent clearer and leverages the compiler's ability to enforce null safety.