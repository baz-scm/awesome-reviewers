---
title: Preserve API Contracts
description: 'When designing API surfaces (typed bindings, bridges, public types),
  ensure you:

  1) Mirror the external API’s calling conventions exactly (constructor vs. method
  parameters, and where “options” belong).'
repository: facebook/react#b11
label: API
language: Rust
comments_count: 2
repository_stars: 251894
---

When designing API surfaces (typed bindings, bridges, public types), ensure you:
1) Mirror the external API’s calling conventions exactly (constructor vs. method parameters, and where “options” belong).
2) Enforce representation invariants at the boundary—don’t let callers construct states that violate the modeled contract.

Practical guidance:
- Validate signatures against the real API: if the external type takes only a callback in its constructor, don’t add extra positional parameters from a different but similar API.
- For public types that represent “unsafe-but-valid” external data (e.g., JS UTF-16 with unpaired surrogates), keep the internal representation private and provide canonical constructors; for read access, prefer borrowed “ref/view” types over exposing internals.

Example (pattern):
```rust
// 1) Correctly model external API shape:
// ResizeObserver: constructor(callback) only; options belong to observe(target, options).

// 2) Encapsulate invariants:
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
    pub fn from_code_units(u: &[u16]) -> Self {
        // canonicalize / enforce the invariant here
        /* ... */
        # unimplemented!()
    }

    pub fn view(&self) -> JsStringRef<'_> {
        /* return borrowed view */
        # unimplemented!()
    }
}
```
This reduces bugs from signature mismatches and prevents invalid states from escaping via the public interface.