---
title: Os-Aware Config Paths
description: When documenting or configuring file system locations and build/package
  filters, ensure the rules match how the software actually resolves paths and applies
  filters on each platform.
repository: cline/cline#v9
label: Configurations
language: Other
comments_count: 2
repository_stars: 70868
---

When documenting or configuring file system locations and build/package filters, ensure the rules match how the software actually resolves paths and applies filters on each platform.

Apply this as a checklist:
- **Use OS-explicit path forms (or document OS-specific expansion).** Don’t assume `~` means the same thing on every OS/shell. For example, Windows users often expect `%USERPROFILE%` semantics.
- **Include all supported plugin/config locations in a way users can copy-paste.** If your app supports both global and project locations plus an additional user directory, represent the user-directory location with OS-correct examples.
- **For ignore/packaging rules, verify against the packaging tool’s real behavior.** If the tool already ignores a pattern (e.g., `**/*.vsix`), don’t keep redundant stale entries—confirm by running the tool’s listing/build inspection (e.g., `vsce ls`) with the rule in place.

Example (doc-friendly, OS-aware):
```md
Global plugins:
- macOS/Linux: `~/.cline/plugins/`
- Windows: `%USERPROFILE%\.cline\plugins\`

Additional user plugins:
- macOS/Linux: `~/Documents/Cline/Plugins/`
- Windows: `%USERPROFILE%\Documents\Cline\Plugins\`
```

Example (packaging verification approach):
- If you remove an ignore rule, first confirm the package output still excludes the artifacts by using the packaging tool’s listing/build inspection commands (rather than relying on memory of its defaults).