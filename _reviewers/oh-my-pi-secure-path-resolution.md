---
title: Secure path resolution
description: When validating or resolving filesystem paths that cross trust boundaries
  (e.g., clone/checkout destinations, or pointer files copied from another repository),
  never trust lexical or unresolved paths — they can be disguised via symlinks or
  `..` traversal to escape intended boundaries or to keep referencing the original
  source's data after a copy....
repository: can1357/oh-my-pi
label: Security
language: Rust
comments_count: 1
repository_stars: 37317
---

When validating or resolving filesystem paths that cross trust boundaries (e.g., clone/checkout destinations, or pointer files copied from another repository), never trust lexical or unresolved paths — they can be disguised via symlinks or `..` traversal to escape intended boundaries or to keep referencing the original source's data after a copy. Canonicalize only the path components that already exist (to correctly follow symlinked ancestors) and treat the final, possibly not-yet-created component literally, since a symlink attack most often targets that last segment. Explicitly reject destinations that resolve inside a protected source tree, and detect/rewrite any embedded references (such as `.git` pointer files) that still resolve into the source's internal metadata after being copied, so the new location cannot silently share or leak state with the source. For example, resolve a destination path by canonicalizing each existing ancestor and only lexically applying the remaining components, then compare the fully resolved path against the forbidden source root before proceeding:

```rust
fn resolve_destination(path: &Path) -> PathBuf {
    let absolute = std::path::absolute(path).unwrap_or_else(|_| path.to_path_buf());
    let mut resolved = PathBuf::new();
    for component in absolute.components() {
        match component {
            Component::ParentDir => { resolved.pop(); },
            Component::Normal(name) => {
                let candidate = resolved.join(name);
                // Only existing components are canonicalized; the final,
                // possibly non-existent entry stays lexical so a symlink
                // there cannot be used to disguise the real destination.
                resolved = fs::canonicalize(&candidate).unwrap_or(candidate);
            },
            _ => {}
        }
    }
    resolved
}

if resolve_destination(dest).starts_with(source_root) {
    return Err(Error::backend("clone", "destination inside source"));
}
```