---
title: optimize data structure operations
description: When working with data structures, prioritize efficiency through proper
  memory management and compact data representation. Use appropriate conversion patterns
  that handle memory cleanup correctly, and leverage bit manipulation techniques for
  space-efficient data storage.
repository: neovim/neovim
label: Algorithms
language: C
comments_count: 2
repository_stars: 91433
---

When working with data structures, prioritize efficiency through proper memory management and compact data representation. Use appropriate conversion patterns that handle memory cleanup correctly, and leverage bit manipulation techniques for space-efficient data storage.

For data structure conversions, ensure proper memory management by clearing source data after copying:
```c
typval_T rv = {
  .vval.v_list = fr_list,
  .v_type = VAR_LIST
};
Object result = vim_to_object(&rv);
tv_clear(&rv);  // Clean up source after conversion
return result;
```

For compact data representation, use bitmasks and enums instead of multiple boolean flags:
```c
enum {
  kCapsLock = 0x02,
  kNumLock = 0x10,
};

// Instead of multiple #ifdef blocks, use:
if (mods & kCapsLock) {
  PUT(*dict, "CapsLock", BOOLEAN_OBJ(true));
}
```

This approach reduces memory overhead, improves cache locality, and makes the code more maintainable while avoiding platform-specific conditional compilation complexity.