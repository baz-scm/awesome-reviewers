---
title: Use constraining types
description: API functions should use specific types and enums to clearly communicate
  valid parameter values rather than accepting arbitrary generic types that suggest
  any value is acceptable.
repository: alacritty/alacritty
label: API
language: Rust
comments_count: 3
repository_stars: 59675
---

API functions should use specific types and enums to clearly communicate valid parameter values rather than accepting arbitrary generic types that suggest any value is acceptable.

When designing function signatures, avoid generic types like `&[u8]`, primitive types, or overly broad parameters when the function only accepts a limited set of valid inputs. Instead, use enums, specific types from relevant libraries, or custom types that encode the constraints directly in the type system.

For example, instead of accepting arbitrary parameters that appear to allow any value:
```rust
// Poor API design - suggests any parameters are valid
fn should_build_esc_key_sequence(
    key: &KeyEvent,
    text: &str,
    mode: TermMode,
    mods: ModifiersState,
) -> bool {
    // Implementation suggests only specific combinations are valid
}
```

Use types that make the valid parameter space explicit:
```rust
// Better API design - constraints are clear from types
enum KeySequenceMode {
    ReportAllKeys,
    DisambiguateEscCodes,
    Standard,
}

fn should_build_esc_key_sequence(
    key: &KeyEvent,
    mode: KeySequenceMode,
) -> bool {
    // Valid inputs are now clear from the signature
}
```

Similarly, prefer specific types from APIs over generic alternatives. Use `LPDWORD` from Windows APIs instead of `*mut u32` when available, or the actual type names rather than generic byte arrays when the function expects specific message formats.

This approach prevents incorrect usage, makes the API self-documenting, and catches invalid parameters at compile time rather than runtime.