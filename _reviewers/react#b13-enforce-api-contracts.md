---
title: Enforce API Contracts
description: When designing or modeling an API surface (including bindings/abstractions
  for external APIs), ensure (a) the interface matches the real contract and (b) public
  types can’t be constructed into invalid states.
repository: facebook/react#b13
label: API
language: Rust
comments_count: 2
repository_stars: 251893
---

When designing or modeling an API surface (including bindings/abstractions for external APIs), ensure (a) the interface matches the real contract and (b) public types can’t be constructed into invalid states.

- Match the contract precisely: verify constructor parameters and where options belong (e.g., constructor vs. method like `observe(target, options)`), instead of copying shapes from similar APIs.
- Encapsulate invariants: don’t expose a representation that lets callers violate required data invariants; provide controlled constructors and safe accessors/views.

Example patterns:
```rust
// Pattern 1: Model the contract correctly
// ResizeObserver(callback) - no second constructor positional param
let resize_observer_ctor = add_function(
    shapes,
    Vec::new(),
    FunctionSignatureBuilder {
        positional_params: vec![Effect::Freeze, Effect::Read],
        ..
    },
);

// Pattern 2: Hide invalid representations behind a controlled API
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
        // canonicalize/enforce surrogate invariant here
        # unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // return a borrowed safe view
        # unimplemented!()
    }
}
```
Use this checklist for any new API surface: confirm signature/option placement against the authoritative spec, and design public types so invariants are enforced by construction, not by caller discipline.