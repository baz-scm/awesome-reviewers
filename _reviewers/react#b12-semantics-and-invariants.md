---
title: Semantics and Invariants
description: 'When exposing an API (types, constructors, function signatures), ensure
  two things: (1) the public surface matches the real underlying contract (correct
  parameters and where options live), and (2) the API cannot be used to create invalid
  internal states (enforce invariants behind safe constructors, and expose views/refs
  for reading).'
repository: facebook/react#b12
label: API
language: Rust
comments_count: 2
repository_stars: 251896
---

When exposing an API (types, constructors, function signatures), ensure two things: (1) the public surface matches the real underlying contract (correct parameters and where options live), and (2) the API cannot be used to create invalid internal states (enforce invariants behind safe constructors, and expose views/refs for reading).

Apply it like this:
- Verify signatures against the true upstream API; don’t copy from similar types without re-checking where arguments/options belong.
- Hide internal representations; provide canonicalizing constructors and safe read-only views so callers can’t bypass invariants.

Example (signature + invariant-safe modeling):
```rust
// (1) Correct contract: callback is the only constructor param.
fn resize_observer_ctor() -> FunctionSignature {
    // No extra positional params; options belong on observe(target, options).
    make_sig(/* positional: [Freeze(callback)] */)
}

// (2) Invariant-safe type: internal repr is private.
pub struct JsString(Repr); // Repr is private

impl JsString {
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize + enforce unpaired surrogate invariant mapping
        JsString(Repr::Wtf16(wtf16_from_code_units(u)))
    }

    pub fn view(&self) -> JsStringRef<'_> { /* borrowed view */ }
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}
```

If a design forces either (a) incorrect parameter placement/signature or (b) public construction that bypasses invariants, redesign the API boundary (signature and/or encapsulation) before shipping.