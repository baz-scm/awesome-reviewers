---
title: API Contracts Must Match
description: When designing API-facing types and bindings (including client/bridge
  globals), ensure the public contract is (a) faithful to the real external API surface
  and (b) impossible to misuse to create invalid states.
repository: facebook/react#b14
label: API
language: Rust
comments_count: 2
repository_stars: 251893
---

When designing API-facing types and bindings (including client/bridge globals), ensure the public contract is (a) faithful to the real external API surface and (b) impossible to misuse to create invalid states.

Apply two checks:
1) Match signatures and option placement exactly
- Verify constructor arity and which calls accept options (e.g., options that belong to `observe(target, options)` must not be modeled as extra constructor parameters).

2) Encapsulate representation to enforce invariants
- Avoid exposing public enums/fields that let callers construct invalid internal states.
- Prefer private representation + safe constructors, and provide borrowed/view types for ergonomics.

Example pattern (invariant-preserving type shape):
```rust
pub struct JsString(Repr);

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>),
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize + enforce wtf16<->unpaired surrogate invariant
        unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // return a borrowed view without exposing invalid construction
        unimplemented!()
    }
}
```

This prevents subtle contract drift (wrong parameter semantics) and misuse (invalid states), improving stability for downstream clients and bridge layers.