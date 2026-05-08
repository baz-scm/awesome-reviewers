---
title: Normalize security inputs
description: For any security-sensitive policy/matching logic (authZ/exec policies,
  allow/deny rules, pattern matching), always canonicalize the relevant inputs before
  matching, and ensure edge cases like absolute-path `..` are handled safely to prevent
  bypass.
repository: Hmbown/DeepSeek-TUI
label: Security
language: Rust
comments_count: 1
repository_stars: 21278
---

For any security-sensitive policy/matching logic (authZ/exec policies, allow/deny rules, pattern matching), always canonicalize the relevant inputs before matching, and ensure edge cases like absolute-path `..` are handled safely to prevent bypass.

Apply:
- Canonicalize paths (trim, normalize separators, and resolve `.`/`..`) before applying glob/prefix/pattern checks.
- Treat absolute paths and `..` consistently (e.g., `/../foo` should normalize to `/foo`, not escape the root).
- Add regression tests for traversal-style bypasses where an attacker reshapes the path to match an overly-permissive pattern.

Example pattern (self-contained):
```rust
fn normalize_path(value: &str) -> String {
    let raw = value.trim().replace('\\', "/");
    let absolute = raw.starts_with('/');

    let mut segs: Vec<&str> = Vec::new();
    for s in raw.split('/') {
        match s {
            "" | "." => {}
            ".." => {
                if !absolute {
                    // For relative paths, preserve leading ..
                    if segs.is_empty() || *segs.last().unwrap() == ".." {
                        segs.push(s);
                    } else {
                        segs.pop();
                    }
                } else {
                    // For absolute paths, clamp: `/../foo` -> `/foo`
                    if !segs.is_empty() && *segs.last().unwrap() != ".." {
                        segs.pop();
                    }
                }
            }
            _ => segs.push(s),
        }
    }

    let mut out = String::new();
    if absolute { out.push('/'); }
    out.push_str(&segs.join("/"));
    out
}

// Security regression test idea:
// assert!(!matches_policy("/src/**", normalize_path("/src/../secret.txt")));
```

This prevents attackers from exploiting normalization gaps to make `/src/../secret.txt` incorrectly match a `/src/**`-style rule.