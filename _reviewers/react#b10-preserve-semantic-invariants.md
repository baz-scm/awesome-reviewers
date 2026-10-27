---
title: Preserve semantic invariants
description: When implementing compiler algorithms that transform program representations,
  ensure you preserve the true semantic inputs (source range semantics and value semantics).
  Avoid deriving critical fields from indices/derived data when the true source-of-truth
  may be missing, placeholder, or lossy—otherwise downstream logic will operate on
  incorrect data.
repository: facebook/react#b10
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 251894
---

When implementing compiler algorithms that transform program representations, ensure you preserve the true semantic inputs (source range semantics and value semantics). Avoid deriving critical fields from indices/derived data when the true source-of-truth may be missing, placeholder, or lossy—otherwise downstream logic will operate on incorrect data.

Apply this standard:
- **Preserve source-of-truth fields:** If a node carries an original offset/range, carry it forward directly. Don’t “reconstruct” offsets from position indices unless you can prove they’re identical in all cases.
- **Guard against placeholder propagation:** If some pipeline stage uses placeholder positions, ensure later conversions either (a) recover the real offsets via stable identity (e.g., node IDs / lookups) or (b) explicitly null/clear derived offset fields so they can’t masquerade as real ranges.
- **Use semantics-preserving value representations:** For character data, choose a string representation that can represent the full set of possible inputs from the source language. If the value can be ill-formed for Rust `String` (e.g., lone surrogates), use a representation that retains those code units and define an explicit wire format across process/bridge layers.
- **Test edge-case invariants:** Add regression tests covering absent/shifted data, collisions/overlapping ranges, nested scopes/bindings, and ill-formed inputs.

Example pattern for the data-mapping side (offsets):
```rust
// Standard: copy the source-of-truth offset, but never let placeholders masquerade as real offsets.
pub(crate) fn convert_base_loc(base: &BaseNode, keep_real: bool) -> Option<SourceLocation> {
    base.loc.as_ref().map(|loc| SourceLocation {
        start: Position { line: loc.start.line, column: loc.start.column, index: loc.start.index },
        end: Position { line: loc.end.line, column: loc.end.column, index: loc.end.index },
        // If upstream used placeholders, do not treat derived offsets as authoritative.
        start_offset: if keep_real { base.start } else { 0 },
    })
}
```

Example pattern for the value side (JS strings):
- Keep valid UTF-8 as the common fast path, but **fallback to a representation that can encode ill-formed cases** (e.g., UTF-16 code units with explicit surrogate markers in the bridge wire format) so computations don’t replace or drop semantic information.