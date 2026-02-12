---
title: Config accuracy and safety
description: 'Confirm that configuration artifacts (docs, config files, and ignore
  lists) match actual runtime behavior and preserve developer workflows.


  Why: Incorrect docs or overly broad ignore rules cause confusion and break common
  development scenarios (hot UI changes, devcontainer editor settings, in-container
  git commits).'
repository: wavetermdev/waveterm
label: Configurations
language: Other
comments_count: 3
repository_stars: 17328
---

Confirm that configuration artifacts (docs, config files, and ignore lists) match actual runtime behavior and preserve developer workflows.

Why: Incorrect docs or overly broad ignore rules cause confusion and break common development scenarios (hot UI changes, devcontainer editor settings, in-container git commits).

How to apply:
- Docs: Verify whether a setting requires an app restart by checking the implementation (frontend vs backend) before documenting. Prefer precise, actionable descriptions. Example correction:
| window:autohidetabbar               | bool     | show and hide the tab bar automatically when the mouse moves near the top of the window

- Ignore files: Don’t broadly exclude files that are needed for developer tooling inside devcontainers (e.g., .vscode, .git, .github). If you must ignore something for image size or build reasons, use targeted patterns or explicit negations and document the reason. Examples:
# keep editor & git metadata for devcontainer workflows
!.vscode
!.git

# still ignore node_modules in image builds
node_modules

- Documentation: When an ignore rule deviates from normal expectations (e.g., removing .git or editor settings), add an inline comment or README note explaining why and how to work around it.

Checklist before committing changes to configs:
- Confirm the runtime effect (restart required?) against the implementation (frontend/backend).
- Run a quick devcontainer test: can you open workspace settings and commit from inside the container?
- If ignoring files, prefer minimal, documented exclusions or maintain separate ignore files for container builds vs repository workflows.

Adopting this rule reduces surprises for developers and ensures configuration changes are both accurate and safe for everyday workflows.