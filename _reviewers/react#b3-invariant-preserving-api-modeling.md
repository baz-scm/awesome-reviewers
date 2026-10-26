---
title: Invariant-Preserving API Modeling
description: 'APIs should be modeled to match the real external contract *and* should
  prevent callers from constructing invalid states via the public surface.


  Apply this standard in two checks:'
repository: facebook/react#b3
label: API
language: Rust
comments_count: 2
repository_stars: 251883
---

APIs should be modeled to match the real external contract *and* should prevent callers from constructing invalid states via the public surface.

Apply this standard in two checks:
1) **Contract accuracy (signatures & semantics):** When modeling external interfaces, verify argument counts and where options belong (e.g., constructor vs. method). Don’t copy a similar type’s shape if the call patterns differ.
2) **Invariant enforcement (public surface):** If a type has validity constraints (e.g., a representation/invariant mapping), avoid exposing construction paths that allow bypassing those invariants. Prefer private internal representations, safe constructors, and borrowed “view” types for reading.

Example pattern (Rust-style):
```rust
pub struct JsString(Repr); // Repr is private

enum Repr {
    Utf8(String),
    Wtf16(Vec<u16>),
}

pub enum JsStringRef<'a> {
    Utf8(&'a str),
    Wtf16(&'a [u16]),
}

impl JsString {
    // Only safe constructors expose valid states.
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize while preserving invariants
        /* ... */
    }

    // Public access uses a borrowed view (no invalid construction).
    pub fn view(&self) -> JsStringRef<'_> {
        match &self.0 {
            Repr::Utf8(s) => JsStringRef::Utf8(s.as_str()),
            Repr::Wtf16(v) => JsStringRef::Wtf16(v.as_slice()),
        }
    }
}
```

Result: your code won’t accidentally model the wrong API shape, and your public types won’t allow callers to create representations that violate required invariants.