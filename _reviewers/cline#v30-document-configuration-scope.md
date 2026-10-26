---
title: Document Configuration Scope
description: 'Ensure configuration behavior is accurately described and safely handled
  across products, rollouts, and workspaces.


  - **Specify scope per product/client**: If different clients enforce different controls,
  state which ones are enforced where and what users can/can’t do.'
repository: cline/cline#v30
label: Configurations
language: Other
comments_count: 3
repository_stars: 70894
---

Ensure configuration behavior is accurately described and safely handled across products, rollouts, and workspaces.

- **Specify scope per product/client**: If different clients enforce different controls, state which ones are enforced where and what users can/can’t do.
- **Document behavior differences by build/rollout**: If toggles mean different things depending on which bundle/build is active, explain the mapping and how to force the bundle with the exact config key.
- **Exclude security-sensitive config artifacts correctly**: Ignore any cached/generated enterprise/remote-config directories that may contain sensitive data, using patterns that match nested workspace folders.
- **Keep ignore/packaging rules non-stale**: Don’t duplicate ignore lists when the packaging tool already excludes the same paths; validate with a quick check.

Example (gitignore):
```gitignore
**/.cline/enterprise/
**/.cline/remote-config/
```
Example (documenting build override):
- “Execute safe commands” vs “Execute commands” depends on which bundle is active; instruct users to set `cline.rollout.bundleOverride` to `next` or `legacy` and reload the window.