---
title: Preserve API Semantics
description: 'Public APIs must (1) match the real interface semantics and (2) preserve
  critical invariants at the boundary.


  Apply this in two ways:


  1) Don’t mis-model constructor signatures'
repository: facebook/react#b5
label: API
language: Rust
comments_count: 2
repository_stars: 251886
---

Public APIs must (1) match the real interface semantics and (2) preserve critical invariants at the boundary.

Apply this in two ways:

1) Don’t mis-model constructor signatures
- Verify which parameters belong to the constructor vs later method calls (e.g., options often move to observe/handle methods, not constructors).
- Avoid copy-pasting parameter lists between similar APIs unless the semantics are identical.

Example pattern (conceptual):
```rust
// Correct: ResizeObserver takes only a callback; {box} goes on observe(target, options).
let resize_observer_ctor = add_function(
    shapes,
    Vec::new(),
    FunctionSignatureBuilder {
        positional_params: vec![Effect::Freeze, Effect::Read],
        ..
    },
);
```

2) Prevent invalid states from being constructible by callers
- If a type must maintain an internal invariant (e.g., a surrogate-marked encoding mapping), don’t expose a public representation that allows bypassing the invariant.
- Prefer validated constructors plus borrowed “view”/ref types for access, rather than letting callers manually create raw variants.

Example pattern (conceptual):
```rust
pub struct JsString(Repr); // Repr kept private

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
        // canonicalize/validate here
        /* ... */
    }

    pub fn view(&self) -> JsStringRef<'_> {
        /* return borrowed view */
    }
}
```

If a review reveals either “wrong parameter belongs in the wrong place” or “callers can construct invalid states,” treat it as an API design bug and fix it by aligning semantics and tightening the boundary invariants.