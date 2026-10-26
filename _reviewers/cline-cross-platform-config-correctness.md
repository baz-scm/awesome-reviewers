---
title: Cross-platform config correctness
description: 'Configuration guidance must be a precise, testable contract across environments:
  don’t assume path expansion semantics (like `~`) work identically on all OSes, and
  don’t duplicate packaging rules that the tooling already enforces.'
repository: Cline/Cline
label: Configurations
language: Other
comments_count: 2
repository_stars: 70840
---

Configuration guidance must be a precise, testable contract across environments: don’t assume path expansion semantics (like `~`) work identically on all OSes, and don’t duplicate packaging rules that the tooling already enforces.

Apply this when updating config docs, plugin search locations, ignore files, or feature flags:
- **Paths**: If you mention or implement user-home locations (e.g., `~/.config`, `~/Documents/...`), ensure the behavior is correct for Windows users too. Either:
  - implement using OS-appropriate path resolution (or documented equivalents), and/or
  - explicitly document the supported Windows locations/profile behaviors (rather than implying `~` is universal).
- **Packaging/filters**: For files like `.vscodeignore`, avoid redundant rules that restate upstream tooling. If the packaging tool already ignores `**/*.vsix`, don’t add duplicate ignores unless you’ve verified they change behavior.
- **Verify**: Validate changes with the packaging/tooling commands that consumers use (e.g., list what will be packaged).

Example (packaging filter sanity check):
```sh
# Create a stale candidate file
mkdir -p dist && touch dist/e2e.vsix

# Verify what will be packaged (do this after changing .vscodeignore)
vsce ls
```

Result: fewer incorrect path assumptions for Windows users, and leaner, more reliable configuration files for packaging and distribution.