---
title: Know your implicit configurations
description: When working with Turborepo, be aware of implicit configurations and
  special files that affect behavior even when not explicitly configured. For example,
  `turbo.json` and `package.json` are always considered inputs when determining if
  a package has changed, even if you try to explicitly ignore them. Package manager
  lockfiles are also always parsed and...
repository: vercel/turborepo
label: Configurations
language: Other
comments_count: 6
repository_stars: 28115
---

When working with Turborepo, be aware of implicit configurations and special files that affect behavior even when not explicitly configured. For example, `turbo.json` and `package.json` are always considered inputs when determining if a package has changed, even if you try to explicitly ignore them. Package manager lockfiles are also always parsed and included in task hashes.

When setting up framework integrations in library packages, use `peerDependencies` in your `package.json` to make framework APIs available without direct installation:

```json
{
  "name": "@repo/ui",
  "peerDependencies": {
    "next": ">=15"
  }
}
```

Note that for older package managers, you may need to configure them to install peer dependencies or add the dependency to `devDependencies` as a workaround.

For repositories without a `packageManager` field, you can use `--dangerously-disable-package-manager-check` or set `dangerouslyDisablePackageManagerCheck: true` in `turbo.json` to bypass lockfile validation, but be aware this can lead to unpredictable behavior as Turborepo will attempt to discover the package manager through best-effort methods.