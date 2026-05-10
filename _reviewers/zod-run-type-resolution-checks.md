---
title: Run Type Resolution Checks
description: Add a CI/pre-release gate that validates your published package’s JavaScript
  + TypeScript type resolution. Use `@arethetypeswrong/cli` to catch broken `exports`/subpath
  import mappings across CJS/ESM and Node versions, and configure it to your supported
  runtime matrix (e.g., ignore known/unavoidable legacy Node failures via `--profile`).
repository: colinhacks/zod
label: CI/CD
language: Json
comments_count: 2
repository_stars: 42628
---

Add a CI/pre-release gate that validates your published package’s JavaScript + TypeScript type resolution. Use `@arethetypeswrong/cli` to catch broken `exports`/subpath import mappings across CJS/ESM and Node versions, and configure it to your supported runtime matrix (e.g., ignore known/unavoidable legacy Node failures via `--profile`).

Example (package-level CI step):
```bash
# install in repo (or as a package devDependency)
# npx @arethetypeswrong/cli --profile node16
# or, if you want multiple profiles:
# npx @arethetypeswrong/cli --profile node16 --profile bundler
```

Apply this when you change `package.json` fields like `exports`, `main/module/types`, or build outputs, so `latest`/release candidates are actually safe for consumers relying on subpath imports.