---
title: Deterministic CI Gates
description: All CI/CD automation should be deterministic, machine-independent, and
  enforced via failing gates—never relying on “latest tag,” unstated baselines, or
  author-local tooling.
repository: warpdotdev/warp
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 56893
---

All CI/CD automation should be deterministic, machine-independent, and enforced via failing gates—never relying on “latest tag,” unstated baselines, or author-local tooling.

Apply these rules:
1) Release automation must compute baselines programmatically
- When building changelogs or diffs for a specific release tag, derive the “previous release cut” for that channel, not the most recent tag overall.
- Encode multi-version releases (e.g., `stable_00/01/02`) explicitly in the baseline-selection logic.

2) Standards should be enforced by CI-run checks
- If a rule is hard to review manually (e.g., “use per-tab theme lookup only inside tab content”), implement a custom lint and run it in presubmit as a hard failure (e.g., dylint with `-D warnings`).

3) Test environments must be reproducible
- Pin required tool versions in CI (e.g., Nushell >= 0.109.0 via pinned Nix input / devshell package).
- CI must assert the required version before smoke tests.
- If the binary/tool is unavailable in CI, explicitly skip those tests rather than depending on local developer configuration.

Example (baseline selection + CI gate sketch):
```rust
// Pseudocode for deterministic “previous cut” lookup
fn previous_cut(tag: &str, all_tags: &[&str]) -> Option<&str> {
    let channel = parse_channel(tag);
    // Filter to same channel, then sort by the release-cut identifier
    // (not by the most recent full tag string).
    let mut cuts = release_cuts_for_channel(channel, all_tags);
    // Find the cut immediately preceding the one containing `tag`
    cuts.find_preceding_cut(tag)
}

// CI (presubmit) should fail on lint violations
// cargo dylint --lib appearance_theme_in_tab_path -- -D warnings
```

Net effect: release artifacts are correct, rules are enforced automatically, and CI results match across machines.