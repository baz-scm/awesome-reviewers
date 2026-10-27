---
title: Config scope and workarounds
description: 'When changing configuration (package/runtime settings, install behavior,
  or config files), make scope explicit and keep changes minimal:


  - Preserve existing runtime behavior with the smallest necessary config tweak (e.g.,
  module type) rather than forcing large refactors.'
repository: facebook/react#b13
label: Configurations
language: Json
comments_count: 3
repository_stars: 251893
---

When changing configuration (package/runtime settings, install behavior, or config files), make scope explicit and keep changes minimal:

- Preserve existing runtime behavior with the smallest necessary config tweak (e.g., module type) rather than forcing large refactors.
- Separate shared configuration from user/local configuration:
  - Commit shared defaults.
  - Add user-specific local files (e.g., `settings.local.json`) to `.gitignore` and provide a shared `settings.json` if some settings should be common.
- For environment-specific dependency/config workarounds:
  - Record why the workaround exists (link to the upstream issue if available).
  - Record how to apply it (e.g., exact install flags like `--ignore-optional`).

Example:
```json
// package.json (minimal runtime/config change to keep existing `require` usage)
{
  "type": "commonjs"
}
```
```gitignore
# user-specific config
settings.local.json
```
```sh
# apply documented workaround for platform/dependency quirks
yarn install --ignore-optional
```