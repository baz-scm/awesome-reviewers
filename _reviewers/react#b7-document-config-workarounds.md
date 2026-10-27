---
title: Document Config Workarounds
description: When changing project configuration (package/module type, dependencies,
  optional deps) to support e2e setup or platform/toolchain quirks, keep the change
  compatible with existing execution behavior and explicitly document the environment-specific
  requirements.
repository: facebook/react#b7
label: Configurations
language: Json
comments_count: 2
repository_stars: 251888
---

When changing project configuration (package/module type, dependencies, optional deps) to support e2e setup or platform/toolchain quirks, keep the change compatible with existing execution behavior and explicitly document the environment-specific requirements.

Apply this by:
- Match runtime/module configuration to current script style (avoid unnecessary refactors). For example, if e2e scripts use `require`, set CommonJS:

```json
{
  "type": "commonjs"
}
```
- For dependency/config changes made to work around known issues on specific platforms, include:
  - the concrete rationale (link or short explanation)
  - the exact install/run instructions needed (e.g., flags affecting optional dependencies)

Example pattern:
- Add the needed dependency/workaround
- Note that on affected environments you must install with the required flags (e.g., `yarn install --ignore-optional`).