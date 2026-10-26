---
title: Validated ignore patterns
description: 'Generated configuration/cache artifacts can be security-sensitive and
  easy to accidentally commit or ship. Standardize on two practices: (1) ignore the
  artifacts correctly across nested repo paths, and (2) validate that build/packaging
  tools also exclude them.'
repository: cline/cline#v21
label: Configurations
language: Other
comments_count: 2
repository_stars: 70886
---

Generated configuration/cache artifacts can be security-sensitive and easy to accidentally commit or ship. Standardize on two practices: (1) ignore the artifacts correctly across nested repo paths, and (2) validate that build/packaging tools also exclude them.

Apply this when you write workspace-side config/caches (e.g., remote configuration snapshots) or produce build outputs that may contain stale packaged files.

**.gitignore: use recursive patterns + verify**
- Use recursive ignore patterns so matches work from any subfolder.
- Add a short comment when the reason is non-obvious (e.g., cached files may contain access keys).
- Verify with `git check-ignore`.

Example:
```gitignore
# Remote config caches (may contain sensitive cached data)
**/.cline/enterprise/
**/.cline/remote-config/
```

**Packaging: rely on tool ignores, but verify with a negative test**
- Don’t add redundant ignore lines without checking existing packager behavior.
- Create a temporary stale artifact (in a local build dir) and confirm it won’t appear in the package using the packager’s listing/inspection commands.

Example verification approach (VS Code extensions):
- Create a fake `dist/e2e.vsix` and run the packager listing (e.g., `vsce ls`) to ensure it’s excluded.

Net effect: you prevent accidental secret/config leakage via git and avoid shipping stale/unwanted artifacts via packaging.