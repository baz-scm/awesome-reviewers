---
title: config hygiene
description: 'Keep repository configuration files canonical, documented, and free
  of personal workspace/debug artifacts.


  Why: Config files determine runtime behavior and developer onboarding. Committing
  personal IDE or temporary debug configs pollutes the repo, causes accidental formatting/behavior
  differences, and hides the canonical way to run the app. Likewise,...'
repository: wavetermdev/waveterm
label: Configurations
language: Json
comments_count: 2
repository_stars: 17328
---

Keep repository configuration files canonical, documented, and free of personal workspace/debug artifacts.

Why: Config files determine runtime behavior and developer onboarding. Committing personal IDE or temporary debug configs pollutes the repo, causes accidental formatting/behavior differences, and hides the canonical way to run the app. Likewise, config schemas consumed by the app should be explicit and stable so tooling/parsers and CI can validate them.

How to apply:
- Do not commit personal workspace or IDE/debug files (e.g., .vscode/launch.json). Add them to .gitignore, or commit a vetted template (e.g., .vscode/launch.json.template) with instructions.
  - Example: remove .vscode/launch.json and document the standard run command: `task electron:dev`.
- Provide and document one canonical method to run services in dev (tasks, npm scripts, Makefile entry). Put those instructions in CONTRIBUTING.md or README_DEV.md so everyone uses the same flow.
- Make config formats explicit and machine-friendly. Add clear fields rather than relying on ad-hoc parsing, and document accepted separators/formatting.
  - Example (from keybindings):
    {
      "command": "app:openConnectionsView",
      "keys": [],
      "commandStr": "/mainview connections"
    }
  Document parsing rules (e.g., comma, whitespace, or '\n' accepted as separators) and enforce via a linter or schema validator in CI.
- If developers need personal debugging conveniences, keep them local (ignored) or provide documented templates and scripts to reproduce behavior without committing per-user files.

Enforcement suggestions:
- Add lints/CI checks that validate config schemas and fail on unexpected workspace/debug files being committed.
- Maintain a small set of canonical templates and clear developer docs for running and debugging the app.

References: discussion indices [0, 1].