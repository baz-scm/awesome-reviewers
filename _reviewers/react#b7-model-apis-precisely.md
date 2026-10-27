---
title: Model APIs Precisely
description: 'When you expose or model an external/spec-driven interface, encode the
  real contract exactly and prevent callers from creating invalid states.


  - Parameter placement must match the real API/spec: don’t copy signatures from similar
  types if the lifecycle differs (e.g., options on `observe(...)` rather than extra
  constructor params).'
repository: facebook/react#b7
label: API
language: Rust
comments_count: 2
repository_stars: 251888
---

When you expose or model an external/spec-driven interface, encode the real contract exactly and prevent callers from creating invalid states.

- Parameter placement must match the real API/spec: don’t copy signatures from similar types if the lifecycle differs (e.g., options on `observe(...)` rather than extra constructor params).
- Public types must enforce their semantic invariants: if a value has a representation constraint required for correctness, don’t expose a raw public representation that allows constructing invalid instances. Prefer private internal reps plus safe constructors/canonicalization, and expose borrowed “view/ref” types for reading.

Example patterns:
```rust
// 1) Signature accuracy: constructor params must reflect the real API.
// ResizeObserver(callback) — options belong to observe(target, options).
let resize_observer_ctor = add_function(
    shapes,
    Vec::new(),
    FunctionSignatureBuilder {
        positional_params: vec![Effect::Freeze, Effect::Read],
        ..
    },
);

// 2) Invariant-safe API: don’t let callers bypass required invariants.
pub struct JsString(Repr); // Repr is private

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>),
}

pub struct JsStringRef<'a> { /* borrowed view */ }

impl JsString {
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize to maintain the invariant
    }

    pub fn view(&self) -> JsStringRef<'_> {
        // borrowed read-only access
    }
}
```