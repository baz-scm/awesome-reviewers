---
title: Explicit build configuration
description: Build-time behavior that depends on versions, paths, or external metadata
  should be configured explicitly and reproducibly—never implicitly via network calls
  or brittle patching.
repository: warpdotdev/warp
label: Configurations
language: Other
comments_count: 3
repository_stars: 56893
---

Build-time behavior that depends on versions, paths, or external metadata should be configured explicitly and reproducibly—never implicitly via network calls or brittle patching.

Apply these rules:
1) Avoid mutable network state during Nix builds/evaluation. If a value (e.g., release/version info) can change, don’t fetch it at build time; instead, pass it as an explicit declared input (or keep it unset and let Nix own upgrades).
2) Prefer configuration knobs (env vars / explicit inputs) over cross-repo string hacks. If another repo needs different paths/behavior for your build, that repo should read an env var and fall back to its current relative defaults.
3) Make pinned external dependencies update-visible. Use explicit flake inputs (even with `flake = false`) so updates go through the normal `flake.lock` workflow instead of hidden `fetchFromGitHub` inside expressions.

Example pattern (replace brittle `substituteInPlace` with upstream env-var overrides):
```rust
// build.rs in warpdotdev/warp-proto-apis (proposed)
use std::path::PathBuf;

fn main() {
  let proto_path = std::env::var("WARP_PROTO_APIS_DIR").ok()
    .map(PathBuf::from)
    .unwrap_or_else(|| {
      // fallback to existing behavior
      let manifest_dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR").unwrap());
      manifest_dir.parent().unwrap().parent().unwrap().to_path_buf()
    });

  println!("cargo:rerun-if-env-changed=WARP_PROTO_APIS_DIR");
  // use proto_path...
}
```
Then in your Nix expression, pass the override:
```nix
substituteInPlace "${./path/to/derivation}" {
  # ...
}
# and ensure the derivation sets the env var, e.g. via buildPhase:
# export WARP_PROTO_APIS_DIR=${warpProtoApis}/apis/multi_agent/v1
```

Outcome: fewer surprising build failures, clearer upgrade semantics, and safer, testable configuration changes across repos.