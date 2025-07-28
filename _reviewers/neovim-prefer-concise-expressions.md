---
title: prefer concise expressions
description: Write concise, readable code by choosing the most direct expression for
  simple operations. Use ternary operators for simple boolean assignments instead
  of verbose if-else blocks, but avoid unnecessary ternaries when direct boolean assignment
  works. Return comparison results directly rather than using intermediate variables
  or verbose conditional blocks.
repository: neovim/neovim
label: Code Style
language: C
comments_count: 5
repository_stars: 91433
---

Write concise, readable code by choosing the most direct expression for simple operations. Use ternary operators for simple boolean assignments instead of verbose if-else blocks, but avoid unnecessary ternaries when direct boolean assignment works. Return comparison results directly rather than using intermediate variables or verbose conditional blocks.

Examples of preferred concise expressions:

```c
// Good: Use ternary for simple assignment
hl.flags |= is_concealed ? kSHConceal : kSHConcealOff;

// Bad: Unnecessary ternary when direct boolean works
bool use_float = strstr(p_cot, "popup") != NULL ? true : false;
// Good: Direct boolean assignment
bool use_float = strstr(p_cot, "popup") != NULL;

// Good: Return comparison directly
return (GetKeyState(VK_CAPITAL) & 0x0001) != 0;

// Bad: Verbose conditional return
if ((GetKeyState(VK_CAPITAL) & 0x0001) != 0) {
  return 1;
} else {
  return 0;
}

// Good: Direct conditional check
if (!os_get_locks_status(&mods, err)) {
  return false;
}

// Bad: Unnecessary intermediate variable
bool status = os_get_locks_status(&mods, err);
if (!status) {
  return false;
}

// Good: Readable comparison order
wlv.char_attr = hl_combine_attr(wlv.vcol < TERM_ATTRS_MAX ? term_attrs[wlv.vcol] : 0, wlv.char_attr);
```

This approach reduces code verbosity while maintaining clarity, making the codebase more maintainable and easier to read.