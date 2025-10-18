---
name: use-proper-types-and-conventions-tensorflow
description: "Enforce clear C++ code in TensorFlow by using explicit types, const-correctness, and other core C++ best practices for performance."
---

# Use Proper Types & Conventions (TensorFlow)

TensorFlow’s C++ codebase has strict style and performance guidelines. Reviewers should emulate these when reviewing C++ (or similar) code:

- **Prefer explicit types over `auto`.** Unless a type is extremely verbose or obvious from context, spell it out. For example, use `int device_ordinal = 0;` instead of `auto device_ordinal = 0;` to make the type clear at a glance[32].
- **Use prefix increment in loops.** In performance-critical loops, use `++i` rather than `i++`. The prefix form can avoid unnecessary copies for iterator types or heavier objects, and TensorFlow code consistently applies this for non-primitive iterators[33].
- **Mark variables and params `const`.** If a variable should not change after initialization, declare it `const`. Similarly, function parameters that aren’t modified should be passed as `const&` or by value if small[34][35]. This communicates intent and can help the compiler optimize.
- **Use modern casts.** Ban C-style casts. Use `static_cast`, `const_cast`, etc., which are safer and more searchable[36]. For example, `static_cast<int64_t>(value)` instead of `(int64_t)value`[37].
- **Maintain comparison order.** Write comparisons as `if (x < 0)` not `if (0 > x)`. Consistency in style makes the codebase easier to read and review[38].

By following these conventions (drawn from Google’s C++ style and practices in TensorFlow), the code will be cleaner, less error-prone, and sometimes even faster. It aligns with the expectations of TensorFlow maintainers, helping any contribution fit in seamlessly[39][33].
